"""
server_tts/tts_engine.py

Server-side TTS using Supertonic 2 ONNX.

Public API:
    ServerTTSEngine(voice, speed, steps, language)
    .speak_filler()
    .feed_token(token)
    .flush()
    .interrupt()
    .resume()
    .is_speaking() → bool
    .wait_until_done(timeout)
    .shutdown()
"""

import re
import threading
import queue
import random
import time

# ── Text helpers ──────────────────────────────────────────────────────────────

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")

MIN_CHUNK_CHARS = 6
MERGE_WINDOW_SEC = 0.05


def _split_sentence(buf: str) -> tuple[str, str]:
    m = _SENTENCE_END.search(buf)
    if m:
        return buf[: m.end()].strip(), buf[m.end() :]
    m = _CLAUSE_BREAK.search(buf)
    if m and m.start() >= MIN_CHUNK_CHARS:
        return buf[: m.start()].strip(), buf[m.end() :]
    return "", buf


def _clean_text(text: str) -> str:
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"_+", "", text)
    text = re.sub(r"`+", "", text)
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
        voice: str = "F1",
        speed: float = 1.0,
        steps: int = 5,
        language: str = "en",
    ):
        self._voice = voice
        self._speed = speed
        self._steps = steps
        self._language = language
        self._model = None  # loaded lazily in worker thread

        self._token_buf = ""
        self._queue = queue.PriorityQueue()
        self._interrupted = threading.Event()
        self._speaking = threading.Event()

        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    # ── Public API ────────────────────────────────────────────────────────────

    def speak_filler(self) -> None:
        self._queue.put(_Item(random.choice(_FILLERS), priority=0))

    def feed_token(self, token: str) -> None:
        if self._interrupted.is_set():
            return
        self._token_buf += token
        while True:
            sentence, remainder = _split_sentence(self._token_buf)
            if sentence and len(sentence) >= MIN_CHUNK_CHARS:
                self._token_buf = remainder
                self._queue.put(_Item(sentence, priority=1))
            else:
                break
        if len(self._token_buf.split()) >= 8:
            text = self._token_buf.strip()
            self._token_buf = ""
            if text:
                self._queue.put(_Item(text, priority=1))

    def flush(self) -> None:
        text = self._token_buf.strip()
        self._token_buf = ""
        if text and len(text) >= 2:
            self._queue.put(_Item(text, priority=1))

    def interrupt(self) -> None:
        self._interrupted.set()
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        from tts.supertonic_model import stop_audio

        stop_audio()

    def resume(self) -> None:
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

    # ── Worker ────────────────────────────────────────────────────────────────

    def _ensure_model(self):
        if self._model is None:
            from tts.supertonic_model import get_model

            self._model = get_model()
            print(
                f"[ServerTTS] Ready — voice={self._voice}, lang={self._language}, steps={self._steps}"
            )

    def _loop(self) -> None:
        self._ensure_model()

        while True:
            item = self._queue.get()
            if item is None:
                break
            if self._interrupted.is_set():
                continue

            collected = [item]
            if item.priority > 0:
                deadline = time.time() + MERGE_WINDOW_SEC
                while time.time() < deadline:
                    try:
                        nxt = self._queue.get_nowait()
                        if nxt is None:
                            self._queue.put(None)
                            break
                        if nxt.priority == 0:
                            self._queue.put(nxt)
                            break
                        collected.append(nxt)
                    except queue.Empty:
                        time.sleep(0.005)

            if self._interrupted.is_set():
                continue

            merged = " ".join(_clean_text(c.text) for c in collected if c.text.strip())
            if not merged:
                continue

            self._speaking.set()
            try:
                from tts.supertonic_model import play_audio

                audio = self._model.generate_one(
                    merged,
                    voice=self._voice,
                    speed=self._speed,
                    steps=self._steps,
                    language=self._language,
                )
                play_audio(audio, self._model.SAMPLE_RATE)
            except Exception as e:
                print(f"[ServerTTS] Error: {e}")
            finally:
                self._speaking.clear()
