"""
transcription/whisper_loader.py
Handles loading the Whisper model exactly once (singleton).
Thread-safe via a lock so the server can handle concurrent requests.
"""

import threading

import torch
import whisper
import whisper.model

from config import WHISPER_MODEL_NAME, WHISPER_MODEL_PATH, WHISPER_DEVICE

_model = None
_lock  = threading.Lock()


def get_model() -> whisper.model.Whisper:
    """
    Return the loaded Whisper model, loading it on first call.
    Thread-safe — safe to call from multiple request threads.
    """
    global _model
    if _model is not None:
        return _model

    with _lock:
        # Double-checked locking: another thread may have loaded it while we waited
        if _model is not None:
            return _model

        print(f"[WhisperLoader] Loading '{WHISPER_MODEL_NAME}' from {WHISPER_MODEL_PATH} ...")
        checkpoint = torch.load(str(WHISPER_MODEL_PATH), map_location="cpu")
        dims  = whisper.model.ModelDimensions(**checkpoint["dims"])
        model = whisper.model.Whisper(dims)
        model.load_state_dict(checkpoint["model_state_dict"])
        model = model.to(WHISPER_DEVICE)
        _model = model
        print(f"[WhisperLoader] Ready on {WHISPER_DEVICE}.")

    return _model


def is_loaded() -> bool:
    return _model is not None