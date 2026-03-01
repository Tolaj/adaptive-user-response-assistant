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
    {"type": "partial",      "text": "..."}   ← only when ENABLE_STT=True
    {"type": "final",        "text": "..."}   ← only when ENABLE_STT=True
    {"type": "llm_start"}
    {"type": "llm_token",    "text": "..."}
    {"type": "llm_done",     "text": "..."}
    {"type": "tts_start"}                     ← only when ENABLE_TTS=True, TTS_MODE="server"
    {"type": "tts_done"}                      ← only when ENABLE_TTS=True, TTS_MODE="server"
    {"type": "pong"}
    {"type": "error",        "message": "..."}
"""

import os, json, time, tempfile, threading
from datetime import datetime
from pathlib import Path
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sock import Sock

from config import WHISPER_MODEL_NAME, WHISPER_SAMPLE_RATE, BASE_DIR
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
from config import (
    ENABLE_STT,
    ENABLE_TTS,
    TTS_MODE,
    TTS_SERVER_BACKEND,
    TTS_KOKORO_VOICE,
    TTS_KOKORO_SPEED,
    TTS_RATE,
    TTS_VOICE_INDEX,
    SHOW_TEXT,
)

# Only import the TTS engine when it might actually be used.
if ENABLE_TTS and TTS_MODE == "server":
    from server_tts.tts_engine import ServerTTSEngine

_SILENCE_THRESHOLD = 0.008
_SILENCE_DURATION = 1.2

# ── Conversation logger ───────────────────────────────────────────────────────

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class ConversationLogger:
    """
    Writes a human-readable log file per session.
    File: logs/conversation_YYYY-MM-DD_HH-MM-SS.log
    Also prints a clean per-request summary to the server console.
    """

    def __init__(self):
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._path = LOGS_DIR / f"conversation_{ts}.log"
        self._req_num = 0
        self._lock = threading.Lock()
        self._session_start = time.time()

        with open(self._path, "w") as f:
            f.write("╔══════════════════════════════════════════════════════╗\n")
            f.write(
                f"  Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write("╚══════════════════════════════════════════════════════╝\n\n")

        print(f"[LOG] Logging to: {self._path}")

    def log_request(
        self,
        user_text: str,
        ai_response: str,
        whisper_latency: float,
        llm_first_token: float,
        llm_total: float,
        end_to_end: float,
    ) -> None:
        with self._lock:
            self._req_num += 1
            num = self._req_num
            ts = datetime.now().strftime("%H:%M:%S")
            session_t = time.time() - self._session_start

            sep = "─" * 54
            print(f"\n  {sep}")
            print(f"  Request #{num:02d}  [{ts}]  (session +{session_t:.0f}s)")
            print(f"  {sep}")
            print(f"  YOU : {user_text}")
            print(f"  AI  : {ai_response}")
            print(f"  {sep}")
            print(f"  ⏱  Whisper     : {whisper_latency:.3f}s")
            print(f"  ⏱  First token : {llm_first_token:.3f}s")
            print(f"  ⏱  LLM total   : {llm_total:.3f}s")
            print(f"  ⏱  End-to-end  : {end_to_end:.3f}s  │  {len(ai_response)} chars")
            print(f"  {sep}\n")

            with open(self._path, "a") as f:
                f.write(f"[{ts}] Request #{num:02d}\n")
                f.write(f"  YOU : {user_text}\n")
                f.write(f"  AI  : {ai_response}\n")
                f.write(f"  TIMERS → whisper:{whisper_latency:.3f}s  ")
                f.write(f"first_token:{llm_first_token:.3f}s  ")
                f.write(f"llm_total:{llm_total:.3f}s  ")
                f.write(f"end_to_end:{end_to_end:.3f}s  ")
                f.write(f"chars:{len(ai_response)}\n\n")

    def log_event(self, event: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        with self._lock:
            print(f"  [LOG] {event}")
            with open(self._path, "a") as f:
                f.write(f"[{ts}] EVENT: {event}\n\n")

    def close(self) -> None:
        duration = time.time() - self._session_start
        with open(self._path, "a") as f:
            f.write("╔══════════════════════════════════════════════════════╗\n")
            f.write(f"  Session ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            f.write(f"  (duration: {duration:.0f}s, {self._req_num} requests)\n")
            f.write("╚══════════════════════════════════════════════════════╝\n")
        print(
            f"[LOG] Session closed — {self._req_num} requests in {duration:.0f}s → {self._path}"
        )


# ── App factory ───────────────────────────────────────────────────────────────


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
                "enable_stt": ENABLE_STT,
                "enable_tts": ENABLE_TTS,
            }
        )

    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        # FIX: respect ENABLE_STT flag on the HTTP transcribe endpoint too.
        if not ENABLE_STT:
            return jsonify({"error": "STT is disabled on this server"}), 503
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
            except Exception:
                pass

    @sock.route("/ws/transcribe")
    def ws_transcribe(ws):
        logger = ConversationLogger()
        logger.log_event("Client connected")

        # FIX: only load Whisper when STT is enabled.
        if ENABLE_STT:
            get_whisper()
        get_llm()

        history = ConversationHistory(max_turns=10)
        silence_samples_need = int(_SILENCE_DURATION * WHISPER_SAMPLE_RATE)
        silence_accumulated = 0
        in_speech = False
        _eos_lock = threading.Lock()

        def send(obj: dict):
            try:
                ws.send(json.dumps(obj))
            except Exception:
                pass

        # ── Server TTS engine ─────────────────────────────────────────────
        # FIX: gate on ENABLE_TTS as well as TTS_MODE.
        # PLAY_SPEECH was imported but never used before — it now acts as a
        # secondary guard so you can keep TTS_MODE="server" but silence output
        # without touching ENABLE_TTS (e.g. for logging-only sessions).
        server_tts = None
        if ENABLE_TTS and TTS_MODE == "server":
            server_tts = ServerTTSEngine(
                backend=TTS_SERVER_BACKEND,
                rate=TTS_RATE,
                voice_index=TTS_VOICE_INDEX,
                voice=TTS_KOKORO_VOICE,
                speed=TTS_KOKORO_SPEED,
            )

        def run_llm(user_text: str, t_eos: float):
            if not user_text.strip():
                return

            # Wait for filler to finish before the main response starts.
            if server_tts:
                server_tts.wait_until_done(timeout=1.5)

            t_llm_start = time.time()
            whisper_lat = t_llm_start - t_eos
            first_token_t = None

            if SHOW_TEXT:
                send({"type": "llm_start"})

            if server_tts:
                server_tts.resume()
                # Tell client the server is about to speak.
                send({"type": "tts_start"})

            full = ""
            first_token = True

            try:
                for token in stream_response(user_text, history):
                    if first_token:
                        first_token_t = time.time() - t_llm_start
                        first_token = False
                    full += token
                    if SHOW_TEXT:
                        send({"type": "llm_token", "text": token})
                    if server_tts:
                        server_tts.feed_token(token)
            finally:
                if server_tts:
                    server_tts.flush()

                t_done = time.time()
                llm_total = t_done - t_llm_start
                e2e = t_done - t_eos

                logger.log_request(
                    user_text=user_text,
                    ai_response=full,
                    whisper_latency=whisper_lat,
                    llm_first_token=first_token_t or llm_total,
                    llm_total=llm_total,
                    end_to_end=e2e,
                )
                if SHOW_TEXT:
                    send({"type": "llm_done", "text": full})

                # Notify client that server speech has ended.
                if server_tts:
                    send({"type": "tts_done"})

        def trigger_eos(force: bool = False):
            nonlocal silence_accumulated, in_speech
            # Discard audio that arrives while the server is speaking — it's
            # just the microphone picking up the TTS output.
            if not force and server_tts and server_tts.is_speaking():
                silence_accumulated = 0
                in_speech = False
                transcriber.clear()
                return
            if not _eos_lock.acquire(blocking=False):
                return
            try:
                t_eos = time.time()
                silence_accumulated = 0
                in_speech = False
                if server_tts:
                    server_tts.interrupt()
                text = transcriber.end_of_speech()
                if text and text.strip():
                    if SHOW_TEXT:
                        send({"type": "final", "text": text})
                    # Fire a filler immediately to bridge LLM latency.
                    if server_tts:
                        server_tts.speak_filler()
                    threading.Thread(
                        target=run_llm, args=(text, t_eos), daemon=True
                    ).start()
            finally:
                _eos_lock.release()

        def on_partial(text: str):
            if SHOW_TEXT:
                send({"type": "partial", "text": text})

        def on_final(text: str):
            pass  # LLM is triggered only via trigger_eos

        # FIX: only create and start the transcriber when STT is enabled.
        transcriber = None
        if ENABLE_STT:
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
                        if ENABLE_STT and transcriber:
                            trigger_eos()
                    elif mtype == "clear_history":
                        history.clear()
                        logger.log_event("Conversation history cleared")
                        send({"type": "pong"})
                    elif mtype == "ping":
                        send({"type": "pong"})
                    continue

                # ── Binary audio frame ────────────────────────────────────
                if isinstance(message, bytes) and len(message) >= 4:
                    # FIX: if STT is disabled, ignore all incoming audio.
                    if not ENABLE_STT or transcriber is None:
                        continue
                    # Drop mic audio while the server is speaking (echo gate).
                    if server_tts and server_tts.is_speaking():
                        silence_accumulated = 0
                        in_speech = False
                        continue
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
            if transcriber:
                transcriber.stop()
            if server_tts:
                server_tts.shutdown()
            logger.log_event("Client disconnected")
            logger.close()

    return app
