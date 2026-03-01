"""
server.py — Flask app + all routes.

WebSocket protocol
──────────────────
Client → Server (binary):  raw float32 LE audio at 16 kHz
Client → Server (JSON):
    {"type": "end_of_speech"}
    {"type": "ping"}
    {"type": "clear_history"}

Server → Client (JSON):
    {"type": "partial",   "text": "..."}
    {"type": "final",     "text": "..."}
    {"type": "llm_start"}
    {"type": "llm_token", "text": "..."}
    {"type": "llm_done",  "text": "..."}
    {"type": "pong"}
    {"type": "error",     "message": "..."}
"""

import os, json, time, tempfile, threading
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sock import Sock

from config import WHISPER_MODEL_NAME, WHISPER_SAMPLE_RATE
from audio.audio_utils import load_audio_as_array
from transcription.whisper_loader import (
    get_model as get_whisper,
    is_loaded as whisper_loaded,
)
from transcription.transcriber import transcribe_audio
from transcription.streaming_transcriber import StreamingTranscriber
from llm.llm_engine import (
    get_llm,
    stream_response,
    ConversationHistory,
    is_loaded as llm_loaded,
)

_SILENCE_THRESHOLD = 0.008
_SILENCE_DURATION = 1.2  # seconds


def create_app() -> Flask:
    app = Flask(__name__)
    sock = Sock(app)
    CORS(app)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            {
                "status": "ok",
                "whisper_loaded": whisper_loaded(),
                "whisper_model": WHISPER_MODEL_NAME,
                "llm_loaded": llm_loaded(),
            }
        )

    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        f = request.files["file"]
        tmp = os.path.join(tempfile.gettempdir(), f"stt_{int(time.time()*1000)}.wav")
        f.save(tmp)
        try:
            get_whisper()
            audio = load_audio_as_array(tmp)
            text = transcribe_audio(audio)
            return jsonify({"text": text})
        except Exception as e:
            import traceback

            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        finally:
            try:
                os.unlink(tmp)
            except:
                pass

    @sock.route("/ws/transcribe")
    def ws_transcribe(ws):
        print("[WS] Client connected")
        get_whisper()
        get_llm()

        history = ConversationHistory(max_turns=10)
        silence_samples_need = int(_SILENCE_DURATION * WHISPER_SAMPLE_RATE)
        silence_accumulated = 0
        in_speech = False

        # Guard so only ONE end_of_speech can trigger the LLM at a time
        _eos_lock = threading.Lock()

        def send(obj: dict):
            try:
                ws.send(json.dumps(obj))
            except Exception:
                pass

        def run_llm(user_text: str, t_eos: float):
            if not user_text.strip():
                return

            t_llm_start = time.time()
            print(f"  [TIMER] Whisper latency  : {t_llm_start - t_eos:.3f}s")

            send({"type": "llm_start"})
            full = ""
            first_token = True
            try:
                for token in stream_response(user_text, history):
                    if first_token:
                        print(
                            f"  [TIMER] LLM first token  : {time.time() - t_llm_start:.3f}s"
                        )
                        first_token = False
                    full += token
                    send({"type": "llm_token", "text": token})
            finally:
                t_done = time.time()
                print(f"  [TIMER] LLM total time   : {t_done - t_llm_start:.3f}s")
                print(f"  [TIMER] End-to-end total : {t_done - t_eos:.3f}s")
                print(f"  [TIMER] Response length  : {len(full)} chars")
                send({"type": "llm_done", "text": full})

        def trigger_eos():
            """
            Single entry point for end-of-speech.
            Uses a lock so client signal and server VAD can't both fire at once.
            """
            nonlocal silence_accumulated, in_speech
            if not _eos_lock.acquire(blocking=False):
                return  # already processing an end-of-speech, skip
            try:
                t_eos = time.time()
                silence_accumulated = 0
                in_speech = False
                text = transcriber.end_of_speech()
                if text and text.strip():
                    send({"type": "final", "text": text})
                    threading.Thread(
                        target=run_llm, args=(text, t_eos), daemon=True
                    ).start()
            finally:
                _eos_lock.release()

        # Whisper partials only — final is handled exclusively via trigger_eos
        def on_partial(text: str):
            send({"type": "partial", "text": text})

        def on_final(text: str):
            # StreamingTranscriber fires this — we only use it to show partials context.
            # The actual LLM trigger comes from trigger_eos() to avoid double calls.
            pass

        transcriber = StreamingTranscriber(
            on_partial=on_partial,
            on_final=on_final,
            sample_rate=WHISPER_SAMPLE_RATE,
        )
        transcriber.start()

        try:
            while True:
                message = ws.receive()
                if message is None:
                    break

                if isinstance(message, str):
                    try:
                        msg = json.loads(message)
                    except json.JSONDecodeError:
                        continue

                    mtype = msg.get("type")
                    if mtype == "end_of_speech":
                        trigger_eos()
                    elif mtype == "clear_history":
                        history.clear()
                        send({"type": "pong"})
                    elif mtype == "ping":
                        send({"type": "pong"})
                    continue

                if isinstance(message, bytes) and len(message) >= 4:
                    chunk = np.frombuffer(message, dtype=np.float32)
                    transcriber.feed(chunk)

                    amp = float(np.abs(chunk).mean())
                    if amp > _SILENCE_THRESHOLD:
                        in_speech = True
                        silence_accumulated = 0
                    elif in_speech:
                        silence_accumulated += len(chunk)
                        if silence_accumulated >= silence_samples_need:
                            trigger_eos()

        except Exception as e:
            print(f"[WS] Error: {e}")
            send({"type": "error", "message": str(e)})
        finally:
            transcriber.stop()
            print("[WS] Client disconnected")

    return app
