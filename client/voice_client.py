"""
client/voice_client.py

Microphone → Smart VAD → WebSocket → Whisper STT → LLM → TTS speaker.
Run:  python -m client.voice_client

Display:
  grey  ... partial transcript while you speak
  blue  YOU: final transcript
  green AI : response text (streamed) + spoken aloud simultaneously

Commands:
  clear  → reset conversation memory
  quit   → exit
"""

import sys
import json
import queue
import threading

import numpy as np
import sounddevice as sd
import resampy
import websocket

from config import RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE
from client.tts_player import create_tts_player

SERVER_WS = "ws://localhost:5001/ws/transcribe"
SERVER_HTTP = "http://localhost:5001/health"

# ── Smart VAD config ──────────────────────────────────────────────────────────
ENERGY_THRESHOLD = 0.015
ZCR_WEIGHT = 0.4
SPEECH_PAD_MS = 150
PAUSE_SECONDS = 1.5
MIN_SPEECH_SEC = 0.4
CHUNK_MS = 30


# ── Smart VAD ─────────────────────────────────────────────────────────────────


class SmartVAD:
    def __init__(self, on_chunk, on_speech_start, on_speech_end):
        self.on_chunk = on_chunk
        self.on_speech_start = on_speech_start
        self.on_speech_end = on_speech_end

        self._pause_samples = int(WHISPER_SAMPLE_RATE * PAUSE_SECONDS)
        self._min_samples = int(WHISPER_SAMPLE_RATE * MIN_SPEECH_SEC)
        self._pad_samples = int(RECORD_SAMPLE_RATE * SPEECH_PAD_MS / 1000)

        self._preroll: list[np.ndarray] = []
        self._preroll_len = 0
        self._in_speech = False
        self._silence_count = 0
        self._speech_samples = 0

    def process(self, chunk: np.ndarray) -> None:
        flat = chunk.flatten()

        self._preroll.append(flat)
        self._preroll_len += len(flat)
        while self._preroll_len > self._pad_samples and self._preroll:
            removed = self._preroll.pop(0)
            self._preroll_len -= len(removed)

        is_speech = self._is_speech(flat)

        if is_speech:
            if not self._in_speech:
                self._in_speech = True
                self._silence_count = 0
                self.on_speech_start()  # ← new: fires when speech begins
                pad = (
                    np.concatenate(self._preroll)
                    if self._preroll
                    else np.array([], dtype=np.float32)
                )
                pad_16k = self._resample(pad)
                if len(pad_16k) > 0:
                    self.on_chunk(pad_16k)
                    self._speech_samples += len(pad_16k)

            chunk_16k = self._resample(flat)
            self.on_chunk(chunk_16k)
            self._speech_samples += len(chunk_16k)
            self._silence_count = 0

        elif self._in_speech:
            chunk_16k = self._resample(flat)
            self.on_chunk(chunk_16k)
            self._silence_count += len(chunk_16k)
            self._speech_samples += len(chunk_16k)

            if self._silence_count >= self._pause_samples:
                if self._speech_samples >= self._min_samples:
                    self.on_speech_end()
                self._in_speech = False
                self._silence_count = 0
                self._speech_samples = 0

    def flush(self):
        if self._in_speech and self._speech_samples >= self._min_samples:
            self.on_speech_end()
        self._in_speech = False
        self._silence_count = 0
        self._speech_samples = 0

    def _is_speech(self, chunk: np.ndarray) -> bool:
        if len(chunk) == 0:
            return False
        energy = float(np.sqrt(np.mean(chunk**2)))
        zcr = (
            float(np.mean(np.abs(np.diff(np.sign(chunk)))) / 2)
            if len(chunk) > 1
            else 0.0
        )
        return (energy + ZCR_WEIGHT * zcr) > ENERGY_THRESHOLD

    @staticmethod
    def _resample(audio: np.ndarray) -> np.ndarray:
        if len(audio) == 0:
            return audio.astype(np.float32)
        if RECORD_SAMPLE_RATE == WHISPER_SAMPLE_RATE:
            return audio.astype(np.float32)
        return resampy.resample(audio, RECORD_SAMPLE_RATE, WHISPER_SAMPLE_RATE).astype(
            np.float32
        )


# ── Terminal display ──────────────────────────────────────────────────────────


class Display:
    _lock = threading.Lock()
    _mid_line = False

    @classmethod
    def partial(cls, text: str):
        with cls._lock:
            print(f"\r  \033[90m... {text:<76}\033[0m", end="", flush=True)
            cls._mid_line = True

    @classmethod
    def you(cls, text: str):
        with cls._lock:
            if cls._mid_line:
                print()
            print(f"  \033[94mYOU:\033[0m {text}", flush=True)
            cls._mid_line = False

    @classmethod
    def ai_start(cls):
        with cls._lock:
            if cls._mid_line:
                print()
            print(f"  \033[92mAI :\033[0m ", end="", flush=True)
            cls._mid_line = True

    @classmethod
    def ai_token(cls, token: str):
        with cls._lock:
            print(token, end="", flush=True)

    @classmethod
    def ai_done(cls):
        with cls._lock:
            print(flush=True)
            cls._mid_line = False

    @classmethod
    def info(cls, text: str):
        with cls._lock:
            if cls._mid_line:
                print()
            print(f"  \033[90m{text}\033[0m", flush=True)
            cls._mid_line = False

    @classmethod
    def error(cls, text: str):
        with cls._lock:
            if cls._mid_line:
                print()
            print(f"  \033[91m[error] {text}\033[0m", flush=True)
            cls._mid_line = False


# ── WebSocket + TTS client ────────────────────────────────────────────────────


class StreamingVoiceClient:
    def __init__(self):
        self._ws: websocket.WebSocketApp | None = None
        self._ws_thread: threading.Thread | None = None
        self._sender_thread: threading.Thread | None = None
        self._connected = threading.Event()
        self._send_q: queue.Queue[bytes | str] = queue.Queue()
        self._running = False

        # TTS — created once, lives for the whole session
        self._tts = create_tts_player()

    def connect(self) -> bool:
        self._ws = websocket.WebSocketApp(
            SERVER_WS,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._ws_thread = threading.Thread(
            target=self._ws.run_forever,
            kwargs={"ping_interval": 20, "ping_timeout": 10},
            daemon=True,
        )
        self._ws_thread.start()
        return self._connected.wait(timeout=10)

    def disconnect(self):
        self._running = False
        self._tts.shutdown()
        if self._ws:
            self._ws.close()

    def send_audio(self, chunk_16k: np.ndarray):
        # Drop audio while TTS is speaking — prevents AI hearing its own voice
        if self._connected.is_set() and not self._tts.is_speaking():
            self._send_q.put(chunk_16k.astype(np.float32).tobytes())

    def send_end_of_speech(self):
        if self._connected.is_set():
            self._send_q.put(json.dumps({"type": "end_of_speech"}))

    def send_clear_history(self):
        if self._connected.is_set():
            self._send_q.put(json.dumps({"type": "clear_history"}))

    def on_user_speech_start(self):
        """Called the moment VAD detects the user started speaking — interrupt TTS."""
        self._tts.interrupt()

    def on_user_speech_end(self):
        """Called when VAD detects user stopped — re-enable TTS."""
        self._tts.resume()

    # ── WebSocket callbacks ───────────────────────────────────────────────

    def _on_open(self, ws):
        Display.info("WebSocket connected")
        self._connected.set()
        self._running = True
        self._sender_thread = threading.Thread(target=self._sender_loop, daemon=True)
        self._sender_thread.start()

    def _on_message(self, ws, message):
        try:
            msg = json.loads(message)
        except Exception:
            return

        t = msg.get("type")
        text = msg.get("text", "")

        if t == "partial":
            if text.strip():
                Display.partial(text)

        elif t == "final":
            if text.strip():
                Display.you(text)

        elif t == "llm_start":
            self._tts.resume()  # re-enable after user spoke
            Display.ai_start()
            # Note: VAD will ignore audio while is_speaking() is True

        elif t == "llm_token":
            # Show text AND feed to TTS simultaneously
            Display.ai_token(text)
            self._tts.feed_token(text)

        elif t == "llm_done":
            # Speak any trailing fragment that didn't end with punctuation
            self._tts.flush()
            Display.ai_done()

        elif t == "error":
            Display.error(msg.get("message", "unknown error"))

    def _on_error(self, ws, error):
        Display.error(f"WS error: {error}")

    def _on_close(self, ws, code, msg):
        self._connected.clear()
        Display.info(f"WebSocket disconnected (code={code})")

    def _sender_loop(self):
        while self._running or not self._send_q.empty():
            try:
                item = self._send_q.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                if isinstance(item, bytes):
                    self._ws.send(item, opcode=websocket.ABNF.OPCODE_BINARY)
                else:
                    self._ws.send(item)
            except Exception as e:
                Display.error(f"Send failed: {e}")
                break


# ── Recording session ─────────────────────────────────────────────────────────


def run_session(client: StreamingVoiceClient) -> None:
    vad = SmartVAD(
        on_chunk=client.send_audio,
        on_speech_start=client.on_user_speech_start,  # interrupt TTS when you speak
        on_speech_end=client.send_end_of_speech,
    )

    def audio_callback(indata, frames, time_info, status):
        vad.process(indata.copy())

    stream = sd.InputStream(
        samplerate=RECORD_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=audio_callback,
        blocksize=int(RECORD_SAMPLE_RATE * CHUNK_MS / 1000),
    )

    stream.start()
    Display.info("🔴  Listening... speak naturally. Press ENTER to stop.")
    input()
    stream.stop()
    stream.close()
    vad.flush()


# ── Command loop ──────────────────────────────────────────────────────────────


def command_loop(client: StreamingVoiceClient) -> None:
    print()
    print(
        "  Commands:  ENTER = start listening  |  'clear' = reset memory  |  'quit' = exit"
    )
    print()

    while True:
        try:
            cmd = input("  [ ENTER to listen, or command ] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd in ("quit", "q"):
            break
        elif cmd == "clear":
            client.send_clear_history()
            Display.info("Conversation history cleared.")
        elif cmd == "":
            print()
            run_session(client)
            print()
        else:
            Display.info(f"Unknown: '{cmd}'  (clear / quit / ENTER)")

    client.disconnect()
    print("\n  Bye!")


# ── Health check ──────────────────────────────────────────────────────────────


def check_server() -> None:
    import requests as req

    try:
        r = req.get(SERVER_HTTP, timeout=5)
        d = r.json()
        print(
            f"  Server OK  |  Whisper: {d['whisper_model']}  |  LLM loaded: {d.get('llm_loaded', '?')}"
        )
    except Exception as e:
        print(f"  Cannot reach server at {SERVER_HTTP}: {e}")
        sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    print("\n" + "=" * 54)
    print("    REAL-TIME VOICE AI  (STT + LLM + TTS)")
    print("=" * 54)
    check_server()

    client = StreamingVoiceClient()
    print("  Connecting WebSocket ...", end="", flush=True)
    if not client.connect():
        print(" FAILED — is the server running?")
        sys.exit(1)
    print(" OK\n")

    print("  Legend:")
    print(
        "  \033[90m... partial\033[0m  |  \033[94mYOU: transcript\033[0m  |  \033[92mAI : response\033[0m"
    )

    command_loop(client)


if __name__ == "__main__":
    main()
