import numpy as np
from config.vad import ENERGY_THRESHOLD
from audio.gate.rms import rms
from audio.gate.zcr import zero_crossing_rate

ZCR_WEIGHT = 0.4


def is_speech_energy(chunk: np.ndarray, threshold: float = ENERGY_THRESHOLD) -> bool:
    if len(chunk) == 0:
        return False
    return (rms(chunk) + ZCR_WEIGHT * zero_crossing_rate(chunk)) > threshold


if __name__ == "__main__":
    import numpy as np

    print(is_speech_energy(np.zeros(1600)))
    print(is_speech_energy(np.random.randn(1600).astype(np.float32) * 0.5))
