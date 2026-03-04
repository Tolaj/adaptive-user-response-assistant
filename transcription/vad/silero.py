import threading
import numpy as np
import torch
from audio.transform.resample import resample
from config.vad import SILERO_THRESHOLD

_model = None
_model_lock = threading.Lock()
_sample_rate = 16000
_MIN_SAMPLES = 512
_accumulator = np.array([], dtype=np.float32)


def _get_model():
    global _model
    if _model is not None:
        return _model
    with _model_lock:
        if _model is not None:
            return _model
        from silero_vad import load_silero_vad

        _model = load_silero_vad()
        _model.reset_states()
    return _model


def is_speech(chunk: np.ndarray, source_sr: int) -> bool:
    global _accumulator
    if len(chunk) == 0:
        return False
    audio = (
        resample(chunk, source_sr, _sample_rate)
        if source_sr != _sample_rate
        else chunk.astype(np.float32)
    )
    _accumulator = np.concatenate([_accumulator, audio])
    if len(_accumulator) < _MIN_SAMPLES:
        return False
    tensor = torch.from_numpy(_accumulator[:_MIN_SAMPLES]).float()
    _accumulator = _accumulator[_MIN_SAMPLES:]
    model = _get_model()
    with _model_lock:
        prob = model(tensor, _sample_rate).item()
    return prob >= SILERO_THRESHOLD
