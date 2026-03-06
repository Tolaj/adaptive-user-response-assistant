# audio/transform/resample.py
import numpy as np
import resampy


def resample(audio: np.ndarray, from_sr: int, to_sr: int) -> np.ndarray:
    """Resample audio using scipy. No-op if rates match."""
    if from_sr == to_sr:
        return audio.astype(np.float32)
    from scipy.signal import resample_poly
    from math import gcd

    g = gcd(from_sr, to_sr)
    return resample_poly(audio, to_sr // g, from_sr // g).astype(np.float32)


if __name__ == "__main__":
    import numpy as np

    a = np.random.randn(44100).astype(np.float32)
    r = resample(a, 44100, 16000)
    print(f"44100 ({len(a)}) → 16000 ({len(r)})")
