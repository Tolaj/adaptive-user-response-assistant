import numpy as np
import soxr


def resample(audio: np.ndarray, from_sr: int, to_sr: int) -> np.ndarray:
    if from_sr == to_sr:
        return audio.astype(np.float32)
    return soxr.resample(audio.astype(np.float32), from_sr, to_sr, quality="HQ")
