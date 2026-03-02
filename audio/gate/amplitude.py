import numpy as np


def mean_amplitude(audio: np.ndarray) -> float:
    """Mean absolute amplitude."""
    return float(np.abs(audio.astype(np.float32)).mean())


if __name__ == "__main__":
    import numpy as np

    print(mean_amplitude(np.array([-0.5, 0.2, 0.8], dtype=np.float32)))
