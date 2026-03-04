# audio/transform/mono.py
import numpy as np


def to_mono(audio: np.ndarray) -> np.ndarray:
    """Convert stereo/multi-channel to mono by averaging channels."""
    if len(audio.shape) > 1:
        return audio.mean(axis=1)
    return audio


if __name__ == "__main__":
    import numpy as np

    stereo = np.random.randn(16000, 2).astype(np.float32)
    print(f"stereo {stereo.shape} → mono {to_mono(stereo).shape}")
