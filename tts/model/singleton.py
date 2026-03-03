import threading

_model: dict | None = None
_lock = threading.Lock()


def get_model() -> dict:
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from tts.download.supertonic import ensure_downloaded
        from tts.model.load import load_supertonic

        _model = load_supertonic(ensure_downloaded())
    return _model


def is_loaded() -> bool:
    return _model is not None
