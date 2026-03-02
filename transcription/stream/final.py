import threading
import numpy as np
import whisper

from transcription.model.singleton import get_model
from transcription.transcribe.options import build_whisper_options
from transcription.hallucination.repetition import has_repetition
from transcription.hallucination.noise import clean_text
from transcription.hallucination.confidence import passes_confidence
from transcription.stream.buffer import get_audio, clear_buffer

from transcription.model.lock import infer_lock as _infer_lock


def run_final_pass(buf: dict) -> str:
    audio = get_audio(buf)
    clear_buffer(buf)
    if audio is None:
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
        print(f"[Final] {e}")
        return ""


if __name__ == "__main__":
    import numpy as np
    from transcription.stream.buffer import create_buffer, append

    buf = create_buffer()
    append(buf, np.zeros(16000, dtype=np.float32))
    print(repr(run_final_pass(buf)))
