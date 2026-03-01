"""
transcription/streaming_transcriber.py

Rolling-buffer streaming transcriber with hallucination suppression.

Hallucination fixes:
  1. no_speech_prob threshold  — Whisper's own confidence score; discard if too low
  2. compression_ratio check   — repeated text compresses heavily; discard if too high
  3. Repetition detector       — if the same phrase appears N+ times, it's a loop
  4. Compression ratio from whisper result — use built-in flag
"""

import re
import threading
import time
from typing import Callable, Optional

import numpy as np
import whisper

from config import WHISPER_DEVICE
from transcription.whisper_loader import get_model

# ── Tuning constants ──────────────────────────────────────────────────────────
MAX_BUFFER_SEC = 29.0  # Whisper hard limit
TRANSCRIBE_EVERY = 0.6  # seconds between partial passes
MIN_AUDIO_SEC = 0.4  # skip transcription for very short clips

NO_SPEECH_THRESHOLD = 0.6  # discard if Whisper says >60% chance no speech
COMPRESSION_RATIO_THRESHOLD = 2.0  # discard if text is suspiciously repetitive
REPETITION_MIN_WORDS = 4  # phrase length to check for repetition
REPETITION_COUNT_THRESHOLD = 3  # how many times a phrase must repeat to be flagged

_infer_lock = threading.Lock()


# ── Hallucination detection ───────────────────────────────────────────────────


def _has_repetition(text: str) -> bool:
    """
    Returns True if the same N-word phrase repeats 3+ times.
    Catches Whisper's looping behaviour like:
      "I'm going to go to the bathroom. I'm going to go to the bathroom. ..."
    """
    words = text.lower().split()
    n = REPETITION_MIN_WORDS

    if len(words) < n * REPETITION_COUNT_THRESHOLD:
        return False

    for start in range(len(words) - n + 1):
        phrase = tuple(words[start : start + n])
        count = 0
        pos = start
        while pos <= len(words) - n:
            if tuple(words[pos : pos + n]) == phrase:
                count += 1
                pos += n
            else:
                pos += 1
        if count >= REPETITION_COUNT_THRESHOLD:
            return True

    return False


def _clean_text(text: str) -> str:
    """Strip leading/trailing whitespace and remove filler-only results."""
    text = text.strip()
    # Whisper sometimes returns just '[BLANK_AUDIO]' or '[ Silence ]' etc.
    if re.match(r"^\[.*\]$", text):
        return ""
    return text


# ── Streaming transcriber ─────────────────────────────────────────────────────


class StreamingTranscriber:
    """
    Feed raw 16 kHz float32 audio via feed().
    Fires on_partial(text) every ~TRANSCRIBE_EVERY seconds.
    Fires on_final(text)   when end_of_speech() is called.
    """

    def __init__(
        self,
        on_partial: Callable[[str], None],
        on_final: Callable[[str], None],
        sample_rate: int = 16000,
    ):
        self.on_partial = on_partial
        self.on_final = on_final
        self.sample_rate = sample_rate

        self._buf: list[np.ndarray] = []
        self._lock = threading.Lock()
        self._last_text = ""
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def feed(self, chunk: np.ndarray) -> None:
        with self._lock:
            self._buf.append(chunk.astype(np.float32))
            # Hard cap — keep under MAX_BUFFER_SEC
            total = sum(len(c) for c in self._buf)
            max_samples = int(MAX_BUFFER_SEC * self.sample_rate)
            while total > max_samples and self._buf:
                dropped = self._buf.pop(0)
                total -= len(dropped)

    def end_of_speech(self) -> str:
        """Transcribe buffer, fire on_final, clear buffer. Returns final text."""
        audio = self._get_audio()
        if audio is None:
            return ""

        text = self._transcribe(audio, is_final=True)

        with self._lock:
            self._buf = []
            self._last_text = ""

        if text:
            self.on_final(text)
        return text

    def clear(self) -> None:
        with self._lock:
            self._buf = []
            self._last_text = ""

    # ── Internals ─────────────────────────────────────────────────────────

    def _loop(self) -> None:
        while self._running:
            time.sleep(TRANSCRIBE_EVERY)
            audio = self._get_audio()
            if audio is None:
                continue
            text = self._transcribe(audio, is_final=False)
            if text and text != self._last_text:
                self._last_text = text
                self.on_partial(text)

    def _get_audio(self) -> Optional[np.ndarray]:
        with self._lock:
            if not self._buf:
                return None
            audio = np.concatenate(self._buf).astype(np.float32)
        if len(audio) / self.sample_rate < MIN_AUDIO_SEC:
            return None
        return audio

    def _transcribe(self, audio: np.ndarray, is_final: bool) -> str:
        model = get_model()
        try:
            with _infer_lock:
                result = whisper.transcribe(
                    model,
                    audio,
                    language="en",
                    fp16=(WHISPER_DEVICE == "cuda"),
                    temperature=0,
                    condition_on_previous_text=False,  # prevents looping context
                    no_speech_threshold=NO_SPEECH_THRESHOLD,
                    compression_ratio_threshold=COMPRESSION_RATIO_THRESHOLD,
                    logprob_threshold=-1.0,
                )

            # ── Hallucination checks ──────────────────────────────────────
            segments = result.get("segments", [])

            # If Whisper flagged all segments as no-speech, discard
            if segments:
                avg_no_speech = sum(s.get("no_speech_prob", 0) for s in segments) / len(
                    segments
                )
                if avg_no_speech > NO_SPEECH_THRESHOLD:
                    return ""

            text = _clean_text(result.get("text", ""))

            if not text:
                return ""

            # Repetition loop detection
            if _has_repetition(text):
                return ""

            return text

        except Exception as e:
            print(f"[StreamingTranscriber] Error: {e}")
            return ""
