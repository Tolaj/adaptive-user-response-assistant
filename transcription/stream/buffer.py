# transcription/stream/buffer.py

import threading
import numpy as np

MAX_BUFFER_SEC = 29.0


def create_buffer(sample_rate: int = 16000) -> dict:
    return {"chunks": [], "lock": threading.Lock(), "sample_rate": sample_rate}


def append(buf: dict, chunk: np.ndarray) -> None:
    with buf["lock"]:
        buf["chunks"].append(chunk.astype(np.float32))
        _cap(buf)


def get_audio(buf: dict) -> np.ndarray | None:
    with buf["lock"]:
        if not buf["chunks"]:
            return None
        return np.concatenate(buf["chunks"]).astype(np.float32)


def clear_buffer(buf: dict) -> None:
    with buf["lock"]:
        buf["chunks"] = []


def _cap(buf: dict) -> None:
    max_samples = int(MAX_BUFFER_SEC * buf["sample_rate"])
    total = sum(len(c) for c in buf["chunks"])
    while total > max_samples and buf["chunks"]:
        total -= len(buf["chunks"].pop(0))
