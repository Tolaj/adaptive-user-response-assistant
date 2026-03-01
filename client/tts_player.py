"""
client/tts_player.py

Two switchable TTS engines:
  "native"  — macOS pyttsx3, zero downloads, instant startup
  "kokoro"  — Kokoro-ONNX neural voice, ~80MB download, much more natural

Switch via config.py:  TTS_ENGINE = "native" | "kokoro"

Both share the same public API so voice_client.py never changes:
  player.feed_token(token)
  player.flush()
  player.interrupt()
  player.resume()
  player.shutdown()
"""

import re
import queue
import threading
import time
from abc import ABC, abstractmethod
from typing import Optional

# ── Sentence splitter (shared) ────────────────────────────────────────────────
_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])\s+|([.?!])$")
_COMMA_PAUSE = re.compile(r",\s+")  # speak on comma too — natural rhythm
MIN_CHUNK_CHARS = 6  # lowered: speak sooner
WORD_TRIGGER = 5  # speak after N words even without punctuation


def _split_sentence(buf: str) -> tuple[str, str]:
    """
    Returns (sentence_to_speak, remaining_buffer).
    Fires on:
      1. Sentence-ending punctuation (.?!)
      2. Comma pause (natural mid-sentence breath)
      3. Word count trigger — speaks after WORD_TRIGGER words even without punctuation
         so the first chunk of speech starts as early as possible.
    """
    # 1. Sentence end
    match = _SENTENCE_END.search(buf)
    if match:
        end = match.end()
        return buf[:end].strip(), buf[end:]

    # 2. Comma pause
    match = _COMMA_PAUSE.search(buf)
    if match and match.start() >= MIN_CHUNK_CHARS:
        end = match.end()
        return buf[: match.start()].strip(), buf[end:]

    # 3. Word-count trigger — dont wait for punctuation
    words = buf.split()
    if len(words) >= WORD_TRIGGER:
        # Cut at the last word boundary so we dont chop a word in half
        cut = buf.rstrip()
        return cut, ""

    return "", buf


# ── Abstract base ─────────────────────────────────────────────────────────────


class BaseTTSPlayer(ABC):
    """
    Shared token-buffering + queue logic.
    Subclasses implement _speak(text) and _stop_current().
    """

    def __init__(self):
        self._token_buf = ""
        self._tts_queue: queue.Queue[Optional[str]] = queue.Queue()
        self._interrupted = threading.Event()
        self._speaking = threading.Event()
        self._running = True

        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    # ── Public API ────────────────────────────────────────────────────────────

    def feed_token(self, token: str) -> None:
        self._token_buf += token
        sentence, self._token_buf = _split_sentence(self._token_buf)
        if sentence and len(sentence) >= MIN_CHUNK_CHARS:
            self._enqueue(sentence)
            # Immediately try again — there may be a second sentence already in buffer
            sentence2, self._token_buf = _split_sentence(self._token_buf)
            if sentence2 and len(sentence2) >= MIN_CHUNK_CHARS:
                self._enqueue(sentence2)

    def flush(self) -> None:
        text = self._token_buf.strip()
        self._token_buf = ""
        if text and len(text) >= 2:
            self._enqueue(text)

    def interrupt(self) -> None:
        self._interrupted.set()
        # Drain queue
        while not self._tts_queue.empty():
            try:
                self._tts_queue.get_nowait()
            except queue.Empty:
                break
        self._stop_current()

    def resume(self) -> None:
        self._interrupted.clear()
        self._token_buf = ""

    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    def shutdown(self) -> None:
        self._running = False
        self._tts_queue.put(None)
        self._worker.join(timeout=5)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _enqueue(self, text: str) -> None:
        if not self._interrupted.is_set():
            self._tts_queue.put(text)

    def _loop(self) -> None:
        self._setup()
        while True:
            item = self._tts_queue.get()
            if item is None:
                break
            if self._interrupted.is_set():
                continue
            self._speaking.set()
            try:
                self._speak(item)
            except Exception as e:
                print(f"[TTS] Error: {e}")
            finally:
                self._speaking.clear()
        self._teardown()

    # ── Subclass interface ────────────────────────────────────────────────────

    def _setup(self) -> None:
        """Called once in worker thread before processing starts."""
        pass

    def _teardown(self) -> None:
        pass

    @abstractmethod
    def _speak(self, text: str) -> None:
        """Speak text synchronously (blocks until done)."""
        ...

    @abstractmethod
    def _stop_current(self) -> None:
        """Interrupt any in-progress speech."""
        ...


# ── Engine 1: macOS native (pyttsx3) ─────────────────────────────────────────


class NativeTTSPlayer(BaseTTSPlayer):
    """
    Uses macOS `say` command via subprocess.
    Works from any thread, no extra dependencies needed.
    """

    def __init__(self, rate: int = 185, volume: float = 1.0, voice_index: int = 0):
        self._rate = rate
        self._voice_index = voice_index
        self._voice_name = None
        self._proc = None
        self._proc_lock = threading.Lock()
        super().__init__()

    def _setup(self) -> None:
        import subprocess

        try:
            out = subprocess.check_output(["say", "-v", "?"], text=True)
            voices = [
                line.split()[0] for line in out.strip().splitlines() if line.strip()
            ]
            self._voice_name = (
                voices[self._voice_index]
                if self._voice_index < len(voices)
                else "Samantha"
            )
            print(
                f"[TTS:native] Ready — voice='{self._voice_name}', rate={self._rate} wpm"
            )
            print(
                f"[TTS:native] Tip: change TTS_VOICE_INDEX in config.py to switch voice"
            )
        except Exception as e:
            self._voice_name = "Samantha"
            print(f"[TTS:native] Using default voice Samantha ({e})")
        # Pre-warm: run a silent say call so the first real call has no startup lag
        try:
            subprocess.run(["say", "-v", self._voice_name, ""], capture_output=True)
        except Exception:
            pass

    def _speak(self, text: str) -> None:
        import subprocess

        cmd = ["say", "-v", self._voice_name, "-r", str(self._rate), text]
        with self._proc_lock:
            self._proc = subprocess.Popen(cmd)
        self._proc.wait()
        with self._proc_lock:
            self._proc = None

    def _stop_current(self) -> None:
        with self._proc_lock:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()


# ── Engine 2: Kokoro-ONNX neural voice ───────────────────────────────────────


class KokoroTTSPlayer(BaseTTSPlayer):
    """
    Uses Kokoro-ONNX for high-quality neural TTS.
    Requires:  pip install kokoro-onnx sounddevice numpy
    First run downloads ~80MB model automatically.

    Voices: af_heart, af_bella, af_sarah, am_adam, am_michael,
            bf_emma, bf_isabella, bm_george, bm_lewis
    """

    def __init__(
        self,
        voice: str = "af_heart",
        speed: float = 1.0,
        lang: str = "en-us",
    ):
        self._voice = voice
        self._speed = speed
        self._lang = lang
        self._kokoro = None
        self._stop_flag = threading.Event()
        super().__init__()

    def _setup(self) -> None:
        try:
            from kokoro_onnx import Kokoro

            print(f"[TTS:kokoro] Loading model (first run downloads ~80MB) ...")
            self._kokoro = Kokoro("kokoro-v0_19.onnx", "voices.json")
            print(f"[TTS:kokoro] Ready — voice={self._voice}, speed={self._speed}")
        except ImportError:
            print("[TTS:kokoro] ERROR: kokoro-onnx not installed.")
            print("             Run:  pip install kokoro-onnx")
            self._kokoro = None
        except Exception as e:
            print(f"[TTS:kokoro] ERROR loading model: {e}")
            self._kokoro = None

    def _speak(self, text: str) -> None:
        if not self._kokoro:
            return

        import sounddevice as sd
        import numpy as np

        self._stop_flag.clear()

        try:
            samples, sample_rate = self._kokoro.create(
                text,
                voice=self._voice,
                speed=self._speed,
                lang=self._lang,
            )

            if self._stop_flag.is_set():
                return

            # Play in small chunks so we can interrupt mid-word
            chunk_size = int(sample_rate * 0.05)  # 50ms chunks
            for i in range(0, len(samples), chunk_size):
                if self._stop_flag.is_set():
                    break
                chunk = samples[i : i + chunk_size]
                sd.play(chunk, samplerate=sample_rate, blocking=True)

        except Exception as e:
            print(f"[TTS:kokoro] Speak error: {e}")

    def _stop_current(self) -> None:
        self._stop_flag.set()
        try:
            import sounddevice as sd

            sd.stop()
        except Exception:
            pass


# ── Factory ───────────────────────────────────────────────────────────────────


def create_tts_player() -> BaseTTSPlayer:
    """
    Creates the TTS player specified by TTS_ENGINE in config.py.
    Falls back to native if kokoro fails to load.
    """
    try:
        from config import (
            TTS_ENGINE,
            TTS_RATE,
            TTS_VOLUME,
            TTS_VOICE_INDEX,
            TTS_KOKORO_VOICE,
            TTS_KOKORO_SPEED,
        )
    except ImportError:
        # Defaults if config doesn't have TTS settings yet
        TTS_ENGINE = "native"
        TTS_RATE = 185
        TTS_VOLUME = 1.0
        TTS_VOICE_INDEX = 0
        TTS_KOKORO_VOICE = "af_heart"
        TTS_KOKORO_SPEED = 1.0

    engine = TTS_ENGINE.lower().strip()

    if engine == "kokoro":
        print("[TTS] Using Kokoro neural engine")
        return KokoroTTSPlayer(
            voice=TTS_KOKORO_VOICE,
            speed=TTS_KOKORO_SPEED,
        )
    else:
        if engine != "native":
            print(f"[TTS] Unknown engine '{engine}', falling back to native")
        return NativeTTSPlayer(
            rate=TTS_RATE,
            volume=TTS_VOLUME,
            voice_index=TTS_VOICE_INDEX,
        )
