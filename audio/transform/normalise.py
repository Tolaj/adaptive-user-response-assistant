import numpy as np


def normalise(audio: np.ndarray) -> np.ndarray:
    """Peak-normalise to [-1, 1]. No-op if silent."""
    peak = np.abs(audio).max()
    if peak > 0:
        return (audio / peak).astype(np.float32)
    return audio.astype(np.float32)


if __name__ == "__main__":
    import numpy as np

    a = np.array([0.1, -0.5, 0.8], dtype=np.float32)
    print(f"before: {a}  after: {normalise(a)}")
