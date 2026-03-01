"""
client/supertonic_player.py

Client-side Supertonic 2 TTS player.

Implements the same interface used by voice_client.py:
    .feed_token(token)
    .flush()
    .interrupt()
    .resume()
    .is_speaking() → bool
    .shutdown()

Design
──────
Supertonic generates a complete audio clip per text chunk (not streaming),
so we use the same sentence-boundary queue + worker thread pattern as the
server-side engine. Tokens are accumulated, split on sentence/clause
boundaries, and queued for the worker which generates + plays each chunk.

A MERGE WINDOW (50 ms) batches same-burst chunks into a single generate()
call so the full response gets natural prosody instead of per-sentence gaps.
"""

import re
import queue
import threading
import time

from config import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

# ── Sentence / clause splitter ────────────────────────────────────────────────

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


# ── Queue item ────────────────────────────────────────────────────────────────


class _Item:
    __slots__ = ("text",)

    def __init__(self, text: str):
        self.text = text


# ── Player ────────────────────────────────────────────────────────────────────


class SupertonicPlayer:
    """
    Client-side Supertonic TTS.

    Usage (same as NativeTTSPlayer / KokoroPlayer):
        player = SupertonicPlayer()
        player.feed_token("Hello ")
        player.feed_token("world!")
        player.flush()
        # ... later ...
        player.interrupt()
        player.resume()
        player.shutdown()
    """

    def __init__(
        self,
        voice: str = SUPERTONIC_VOICE,
        language: str = SUPERTONIC_LANGUAGE,
        steps: int = SUPERTONIC_STEPS,
        speed: float = SUPERTONIC_SPEED,
    ):
        self._voice = voice
        self._language = language
        self._steps = steps
        self._speed = speed

        self._token_buf = ""
        self._queue: queue.Queue[_Item | None] = queue.Queue()
        self._interrupted = threading.Event()
        self._speaking = threading.Event()
        self._model = None  # loaded lazily in worker thread

        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    # ── Public interface ──────────────────────────────────────────────────────

    def feed_token(self, token: str) -> None:
        """Accumulate token; push complete sentences/clauses to the queue."""
        if self._interrupted.is_set():
            return
        self._token_buf += token
        while True:
            sentence, remainder = _split_sentence(self._token_buf)
            if sentence and len(sentence) >= MIN_CHUNK_CHARS:
                self._token_buf = remainder
                self._queue.put(_Item(sentence))
            else:
                break
        # Safety flush at 8 words for long run-on sentences
        if len(self._token_buf.split()) >= 8:
            text = self._token_buf.strip()
            self._token_buf = ""
            if text:
                self._queue.put(_Item(text))

    def flush(self) -> None:
        """Push any remaining buffer at end of LLM stream."""
        text = self._token_buf.strip()
        self._token_buf = ""
        if text and len(text) >= 2:
            self._queue.put(_Item(text))

    def interrupt(self) -> None:
        """Stop playback immediately and drain the pending queue."""
        self._interrupted.set()
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        from tts.supertonic_model import stop_audio

        stop_audio()

    def resume(self) -> None:
        """Clear interrupted flag; must be called before the next feed_token()."""
        self._token_buf = ""
        self._interrupted.clear()

    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    def shutdown(self) -> None:
        self.interrupt()
        self._queue.put(None)  # sentinel to exit worker
        self._worker.join(timeout=3)

    # ── Worker ────────────────────────────────────────────────────────────────

    def _ensure_model(self):
        if self._model is None:
            from tts.supertonic_model import get_model

            self._model = get_model()

    def _loop(self) -> None:
        # Load model once (in the worker thread, not the main thread)
        self._ensure_model()

        while True:
            item = self._queue.get()
            if item is None:
                break
            if self._interrupted.is_set():
                continue

            # ── MERGE WINDOW ──────────────────────────────────────────────────
            # Batch chunks arriving within 50 ms into one generate() call so a
            # full response gets natural prosody and fewer synthesis round-trips.
            collected = [item]
            deadline = time.time() + MERGE_WINDOW_SEC
            while time.time() < deadline:
                try:
                    nxt = self._queue.get_nowait()
                    if nxt is None:
                        self._queue.put(None)
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
                audio = self._model.generate_one(
                    merged,
                    voice=self._voice,
                    speed=self._speed,
                    steps=self._steps,
                    language=self._language,
                )
                from tts.supertonic_model import play_audio

                play_audio(audio, self._model.SAMPLE_RATE)
            except Exception as e:
                print(f"[SupertonicPlayer] Error: {e}")
            finally:
                self._speaking.clear()
