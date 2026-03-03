# transcription/model/__init__.py
from transcription.model.singleton import get_model, is_loaded, reset
from transcription.model.device import resolve_device
from transcription.model.lock import infer_lock
