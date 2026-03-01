"""
client/vad.py
Voice Activity Detection state machine.

Two firing modes:
  1. Silence boundary  — fires when speech is followed by N seconds of silence (short utterances)
  2. Rolling window    — fires every ROLLING_WINDOW_SEC while you keep talking (long utterances)
     After a rolling flush the buffer is cleared so the next chunk is fresh.
"""

from typing import Callable

import numpy as np

from config import (
    RECORD_SAMPLE_RATE,
    SILENCE_THRESHOLD,
    SILENCE_DURATION,
    MIN_SPEECH,
    ROLLING_WINDOW_SEC,
)


class VADProcessor:
    """
    Stateful VAD processor.  Feed audio chunks via process_chunk().
    Fires on_speech_end with a float32 numpy array when:
      - silence boundary is detected (end of utterance), OR
      - speech has been continuous for ROLLING_WINDOW_SEC seconds.

    Parameters
    ----------
    on_speech_end     : callable(np.ndarray)
    sample_rate       : int
    silence_threshold : float
    silence_duration  : float   seconds of silence → end of utterance
    min_speech        : float   minimum utterance length to emit
    rolling_window    : float   emit mid-utterance every N seconds of continuous speech
    """

    def __init__(
        self,
        on_speech_end:     Callable[[np.ndarray], None],
        sample_rate:       int   = RECORD_SAMPLE_RATE,
        silence_threshold: float = SILENCE_THRESHOLD,
        silence_duration:  float = SILENCE_DURATION,
        min_speech:        float = MIN_SPEECH,
        rolling_window:    float = ROLLING_WINDOW_SEC,
    ):
        self.on_speech_end     = on_speech_end
        self.sample_rate       = sample_rate
        self.silence_threshold = silence_threshold
        self.silence_need      = int(silence_duration  * sample_rate)
        self.speech_need       = int(min_speech        * sample_rate)
        self.rolling_need      = int(rolling_window    * sample_rate)

        self._reset()

    # ── Public API ────────────────────────────────────────────────────────────

    def process_chunk(self, chunk: np.ndarray) -> None:
        """Feed one audio block (float32, mono)."""
        flat = chunk.flatten()
        amp  = float(np.abs(flat).mean())

        if amp > self.silence_threshold:
            # ── Active speech ──────────────────────────────────────────────
            self._in_speech = True
            self._speech_buf.append(flat)
            self._silence_buf = []

            # Rolling window: emit if we've accumulated enough continuous speech
            speech_samples = sum(len(f) for f in self._speech_buf)
            if speech_samples >= self.rolling_need:
                audio = np.concatenate(self._speech_buf).astype(np.float32)
                self._speech_buf  = []   # clear — next window starts fresh
                self._silence_buf = []
                # keep _in_speech = True so recording continues uninterrupted
                self.on_speech_end(audio)

        elif self._in_speech:
            # ── Trailing silence after speech ──────────────────────────────
            self._silence_buf.append(flat)
            self._speech_buf.append(flat)

            silence_samples = sum(len(f) for f in self._silence_buf)
            if silence_samples >= self.silence_need:
                self._flush()

    def flush(self) -> None:
        """Force-flush any buffered speech (e.g. on stream stop)."""
        if self._in_speech and self._speech_buf:
            self._flush()

    # ── Internals ─────────────────────────────────────────────────────────────

    def _flush(self) -> None:
        audio = np.concatenate(self._speech_buf).astype(np.float32)
        self._reset()
        if len(audio) >= self.speech_need:
            self.on_speech_end(audio)

    def _reset(self) -> None:
        self._in_speech   = False
        self._speech_buf  = []
        self._silence_buf = []