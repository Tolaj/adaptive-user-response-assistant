"""
server_tts/tts_engine.py

Server-side TTS using macOS `say` command via subprocess.

Why not AppKit NSSpeechSynthesizer?
  - Its delegate callback (didFinishSpeaking) requires NSRunLoop
  - Daemon threads have no NSRunLoop → callback never fires → blocks forever

Why subprocess `say` works:
  - Works from any thread, always
  - Pre-warmed by running one silent call at startup
  - Per-call overhead ~30ms after pre-warm — fast enough

Architecture:
  - One persistent worker thread processes TTS queue in order
  - speak_filler() fires immediately, no buffering
  - feed_token() accumulates until sentence boundary, then speaks
  - interrupt() kills current subprocess and drains queue instantly
"""

import re
import threading
import queue
import subprocess
import random
import time
from typing import Optional


# ── Sentence splitter ─────────────────────────────────────────────────────────
_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])\s+|([.?!])$")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")
MIN_CHUNK_CHARS = 10


def _split_sentence(buf: str) -> tuple[str, str]:
    match = _SENTENCE_END.search(buf)
    if match:
        return buf[: match.end()].strip(), buf[match.end() :]
    match = _CLAUSE_BREAK.search(buf)
    if match and match.start() >= MIN_CHUNK_CHARS:
        return buf[: match.start()].strip(), buf[match.end() :]
    return "", buf


# ── Filler phrases ────────────────────────────────────────────────────────────
_FILLERS = [
    "Mm-hmm.",
    "Sure.",
    "Okay.",
    "Right.",
    "Mm.",
    "Yeah.",
    "I see.",
    "Got it.",
    "Ah.",
    "Sure thing.",
]


# ── Engine ────────────────────────────────────────────────────────────────────


class ServerTTSEngine:

    def __init__(
        self,
        backend: str = "native",
        rate: int = 170,
        voice_index: int = 138,
        voice: str = "af_heart",
        speed: float = 1.0,
    ):
        self._rate = rate
        self._voice_index = voice_index

        self._token_buf = ""
        self._queue: queue.Queue[Optional[str]] = queue.Queue()
        self._interrupted = threading.Event()
        self._speaking = threading.Event()
        self._proc = None
        self._proc_lock = threading.Lock()
        self._voice_name = "Samantha"  # resolved in _setup

        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    # ── Public API ────────────────────────────────────────────────────────────

    def speak_filler(self) -> None:
        """Speak an instant acknowledgment to bridge LLM thinking time."""
        if not self._interrupted.is_set():
            self._queue.put(random.choice(_FILLERS))

    def feed_token(self, token: str) -> None:
        self._token_buf += token
        while True:
            sentence, remainder = _split_sentence(self._token_buf)
            if sentence and len(sentence) >= MIN_CHUNK_CHARS:
                self._token_buf = remainder
                if not self._interrupted.is_set():
                    self._queue.put(sentence)
            else:
                break
        # Safety flush if buffer grows very long with no punctuation
        if len(self._token_buf.split()) >= 12:
            text = self._token_buf.strip()
            self._token_buf = ""
            if text and not self._interrupted.is_set():
                self._queue.put(text)

    def flush(self) -> None:
        text = self._token_buf.strip()
        self._token_buf = ""
        if text and len(text) >= 2 and not self._interrupted.is_set():
            self._queue.put(text)

    def interrupt(self) -> None:
        self._interrupted.set()
        # Drain queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        # Kill current subprocess
        with self._proc_lock:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=0.5)
                except:
                    pass

    def resume(self) -> None:
        self._interrupted.clear()
        self._token_buf = ""

    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    def wait_until_done(self, timeout: float = 2.0) -> None:
        """Block until current speech finishes (used to let filler complete)."""
        deadline = time.time() + timeout
        # Give queue time to start
        time.sleep(0.05)
        while self.is_speaking() and time.time() < deadline:
            time.sleep(0.02)

    def shutdown(self) -> None:
        self.interrupt()
        self._queue.put(None)
        self._worker.join(timeout=3)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _loop(self) -> None:
        self._setup()
        while True:
            item = self._queue.get()
            if item is None:
                break
            if self._interrupted.is_set():
                continue
            self._speaking.set()
            try:
                self._say(item)
            except Exception as e:
                print(f"[ServerTTS] Error: {e}")
            finally:
                self._speaking.clear()

    def _setup(self) -> None:
        try:
            out = subprocess.check_output(["say", "-v", "?"], text=True, timeout=5)
            voices = [
                line.split()[0] for line in out.strip().splitlines() if line.strip()
            ]
            self._voice_name = (
                voices[self._voice_index]
                if self._voice_index < len(voices)
                else "Samantha"
            )
        except Exception:
            self._voice_name = "Samantha"

        # Pre-warm: first say call has ~200ms overhead, subsequent ones ~30ms
        try:
            subprocess.run(
                ["say", "-v", self._voice_name, "-r", str(self._rate), ""],
                capture_output=True,
                timeout=3,
            )
        except Exception:
            pass

        print(f"[ServerTTS] Ready — voice={self._voice_name}, rate={self._rate} wpm")

    def _say(self, text: str) -> None:
        """Speak text synchronously via `say`. Blocks until done or interrupted."""
        cmd = ["say", "-v", self._voice_name, "-r", str(self._rate), text]
        with self._proc_lock:
            if self._interrupted.is_set():
                return
            self._proc = subprocess.Popen(cmd)
        self._proc.wait()
        with self._proc_lock:
            self._proc = None
