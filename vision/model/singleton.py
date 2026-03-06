import threading
from config.vlm import VLM_BACKEND

_model = None
_server_proc = None
_lock = threading.Lock()


def get_model():
    global _model, _server_proc
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from vision.model.load import load_vlm

        result = load_vlm()
        if VLM_BACKEND == "server":
            _server_proc = result
            _model = True  # sentinel — actual calls go via HTTP
        else:
            _model = result
    return _model


def get_server_proc():
    return _server_proc


def is_loaded() -> bool:
    return _model is not None


def shutdown():
    global _model, _server_proc
    if _server_proc:
        _server_proc.terminate()
        _server_proc = None
    _model = None
