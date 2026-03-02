import threading
from typing import Optional
import whisper.model as wm

_model: Optional[wm.Whisper] = None
_lock = threading.Lock()


def get_model() -> wm.Whisper:
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from transcription.model.load import load_whisper

        _model = load_whisper()
    return _model


def is_loaded() -> bool:
    return _model is not None


def reset():
    global _model
    _model = None
