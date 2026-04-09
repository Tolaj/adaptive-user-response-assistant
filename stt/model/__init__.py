# transcription/model/__init__.py
from stt.model.singleton import get_model, is_loaded, reset
from stt.model.device import resolve_device
from stt.model.lock import infer_lock
