# transcription/stream/partial.py
import threading
import numpy as np
import whisper

from transcription.model.singleton import get_model
from transcription.transcribe.options import build_whisper_options
from transcription.hallucination.repetition import has_repetition
from transcription.hallucination.noise import clean_text
from transcription.hallucination.confidence import passes_confidence
from config.vad import MIN_AUDIO_SEC

from transcription.model.lock import infer_lock as _infer_lock


def run_partial_pass(buf: dict) -> str:
    from transcription.stream.buffer import get_audio

    audio = get_audio(buf)
    if audio is None or len(audio) / buf["sample_rate"] < MIN_AUDIO_SEC:
        return ""
    return _transcribe(audio)


def _transcribe(audio: np.ndarray) -> str:
    try:
        with _infer_lock:
            result = whisper.transcribe(get_model(), audio, **build_whisper_options())
        if not passes_confidence(result):
            return ""
        text = clean_text(result.get("text", ""))
        return "" if (not text or has_repetition(text)) else text
    except Exception as e:
        print(f"[Partial] {e}")
        return ""
