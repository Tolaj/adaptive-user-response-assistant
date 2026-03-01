"""
transcription/transcriber.py
Pure transcription logic — takes a numpy audio array, returns text.
Decoupled from Flask and from file I/O.
"""

import threading
import time

import numpy as np
import whisper

from config import WHISPER_DEVICE
from transcription.whisper_loader import get_model

# One lock so GPU calls never overlap
_infer_lock = threading.Lock()


def transcribe_audio(audio: np.ndarray) -> str:
    """
    Transcribe a 16 kHz float32 mono numpy array.
    Returns the transcribed string (stripped).
    Raises on Whisper errors — callers should handle exceptions.
    """
    model = get_model()

    duration = len(audio) / 16_000
    print(f"[Transcriber] Transcribing {duration:.1f}s of audio ...", flush=True)

    t0 = time.time()
    with _infer_lock:
        result = whisper.transcribe(
            model,
            audio,
            language="en",
            fp16=(WHISPER_DEVICE == "cuda"),
            temperature=0,
            condition_on_previous_text=True,
        )

    text = result["text"].strip()
    print(f"[Transcriber] '{text}'  ({time.time() - t0:.2f}s)", flush=True)
    return text