# transcription/transcribe/batch.py
import time
import threading

import numpy as np
import whisper

from transcription.model.singleton import get_model
from config.whisper import WHISPER_DEVICE

from transcription.model.lock import infer_lock as _infer_lock


def transcribe_audio(audio: np.ndarray) -> str:
    """
    One-shot transcription of a 16 kHz float32 mono array.
    Returns stripped transcript string. Raises on error.
    """
    model = get_model()
    duration = len(audio) / 16_000
    print(f"[Transcribe] {duration:.1f}s ...", flush=True)
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
    print(f"[Transcribe] '{text}'  ({time.time()-t0:.2f}s)", flush=True)
    return text


if __name__ == "__main__":
    import numpy as np

    audio = np.zeros(16000, dtype=np.float32)
    print(repr(transcribe_audio(audio)))
