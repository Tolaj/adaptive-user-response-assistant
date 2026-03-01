"""
server_tts/tts_engine.py

Server-side TTS using macOS `say` command via subprocess.

FIX v4 — Missing words / clipped speech
─────────────────────────────────────────
Root cause: each text chunk was a separate `say` subprocess call.
Each call has ~30ms startup overhead AND the synthesizer resets its
prosody context between calls — so word boundaries at chunk edges get
clipped or swallowed entirely. For example:

  chunk 1: "Sure thing!"        → spoken fine
  chunk 2: "Here's one:"        → leading "H" clipped (say startup gap)
  chunk 3: "Why don't..."       → "W" clipped
  flush:   "everything!"        → may be swallowed entirely if tiny

Fix: use a MERGE WINDOW in the worker loop. Instead of speaking each
queue item immediately, the worker collects all items that arrive within
MERGE_WINDOW_MS (50 ms) and concatenates them into a single `say` call.
This means a full LLM response like:
  "Sure thing! Here's one: Why don't scientists trust atoms?"
is spoken as ONE subprocess call with natural prosody throughout.

For responses that stream slowly (one sentence every 300ms), each
sentence still gets its own `say` call, but that's fine — the boundary
is a real sentence break with natural pause anyway.

Interrupt still kills the subprocess immediately via SIGTERM.
"""

import re
import threading
import queue
import subprocess
import random
import time
from typing import Optional


# ── Sentence splitter ─────────────────────────────────────────────────────────

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")

# Minimum chars before we consider a chunk "speakable" on its own.
# Kept small so the first sentence fires quickly.
MIN_CHUNK_CHARS = 6

# How long (seconds) the worker waits for more chunks before speaking.
# 50 ms is imperceptible as latency but catches same-burst chunks.
MERGE_WINDOW_SEC = 0.05


def _split_sentence(buf: str) -> tuple[str, str]:
    match = _SENTENCE_END.search(buf)
    if match:
        return buf[: match.end()].strip(), buf[match.end() :]
    match = _CLAUSE_BREAK.search(buf)
    if match and match.start() >= MIN_CHUNK_CHARS:
        return buf[: match.start()].strip(), buf[match.end() :]
    return "", buf


def _clean_for_say(text: str) -> str:
    """Remove characters that confuse `say` or cause it to skip words."""
    # Remove markdown-style formatting
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"_+", "", text)
    text = re.sub(r"`+", "", text)
    # Collapse multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)
    return text.strip()


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


# ── Priority queue item ───────────────────────────────────────────────────────


class _Item:
    """priority=0 → filler (plays first), priority=1 → normal LLM sentence."""

    __slots__ = ("priority", "text")

    def __init__(self, text: str, priority: int = 1):
        self.priority = priority
        self.text = text

    def __lt__(self, other: "_Item") -> bool:
        return self.priority < other.priority


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
        self._queue: queue.PriorityQueue = queue.PriorityQueue()
        self._interrupted = threading.Event()
        self._speaking = threading.Event()
        self._proc = None
        self._proc_lock = threading.Lock()
        self._voice_name = "Samantha"

        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    # ── Public API ────────────────────────────────────────────────────────────

    def speak_filler(self) -> None:
        """
        Enqueue a filler at high priority.
        Caller must call resume() before this — see trigger_eos() in server.py.
        """
        self._queue.put(_Item(random.choice(_FILLERS), priority=0))

    def feed_token(self, token: str) -> None:
        """Accumulate token and flush complete sentences/clauses to the queue."""
        self._token_buf += token
        while True:
            sentence, remainder = _split_sentence(self._token_buf)
            if sentence and len(sentence) >= MIN_CHUNK_CHARS:
                self._token_buf = remainder
                self._queue.put(_Item(sentence, priority=1))
            else:
                break
        # Safety flush at 8 words for long run-on sentences
        if len(self._token_buf.split()) >= 8:
            text = self._token_buf.strip()
            self._token_buf = ""
            if text:
                self._queue.put(_Item(text, priority=1))

    def flush(self) -> None:
        """Push any remaining buffer to the queue at end of LLM stream."""
        text = self._token_buf.strip()
        self._token_buf = ""
        if text and len(text) >= 2:
            self._queue.put(_Item(text, priority=1))

    def interrupt(self) -> None:
        """Stop current speech and drain the queue."""
        self._interrupted.set()
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        with self._proc_lock:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=0.5)
                except Exception:
                    pass

    def resume(self) -> None:
        """
        Clear interrupted flag. MUST be called before speak_filler() /
        feed_token() — see server.py trigger_eos() for correct order.
        """
        self._token_buf = ""
        self._interrupted.clear()

    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    def wait_until_done(self, timeout: float = 2.0) -> None:
        deadline = time.time() + timeout
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
            # Block until first item arrives
            item = self._queue.get()
            if item is None:
                break
            if self._interrupted.is_set():
                continue

            # ── MERGE WINDOW ─────────────────────────────────────────────
            # Collect additional chunks that arrive within MERGE_WINDOW_SEC.
            # This prevents per-chunk subprocess gaps that clip word edges.
            # Filler items (priority=0) are never merged — they speak alone
            # so they don't get delayed by waiting for LLM chunks.
            collected = [item]
            if item.priority > 0:  # don't delay fillers
                deadline = time.time() + MERGE_WINDOW_SEC
                while time.time() < deadline:
                    try:
                        next_item = self._queue.get_nowait()
                        if next_item is None:
                            # Put sentinel back and stop collecting
                            self._queue.put(None)
                            break
                        if next_item.priority == 0:
                            # Filler arrived — speak it next, stop merging
                            # Put filler back at front (it has lower priority
                            # number so PriorityQueue will return it first)
                            self._queue.put(next_item)
                            break
                        collected.append(next_item)
                    except queue.Empty:
                        time.sleep(0.005)

            if self._interrupted.is_set():
                continue

            # Join all collected chunks into one `say` call
            merged_text = " ".join(
                _clean_for_say(c.text) for c in collected if c.text.strip()
            )
            if not merged_text:
                continue

            self._speaking.set()
            try:
                self._say(merged_text)
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

        # Pre-warm: first `say` call has ~200ms overhead; subsequent ~30ms
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
