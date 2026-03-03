# audio/gate/rms.py
import numpy as np


def rms(audio: np.ndarray) -> float:
    """Root mean square energy."""
    return float(np.sqrt(np.mean(audio.astype(np.float32) ** 2)))


if __name__ == "__main__":
    import numpy as np

    print(f"silence: {rms(np.zeros(1000)):.4f}")
    print(f"speech:  {rms(np.random.randn(1000).astype(np.float32) * 0.3):.4f}")
