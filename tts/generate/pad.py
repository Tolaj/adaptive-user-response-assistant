import numpy as np

PRE_PAD_SEC = 0.03
POST_PAD_SEC = 0.08


def apply_padding(audio: np.ndarray, sample_rate: int) -> np.ndarray:
    """Prepend 30 ms + append 80 ms of silence. Prevents clipping at both edges."""
    pre = np.zeros(int(sample_rate * PRE_PAD_SEC), dtype=np.float32)
    post = np.zeros(int(sample_rate * POST_PAD_SEC), dtype=np.float32)
    return np.concatenate([pre, audio.astype(np.float32), post])


if __name__ == "__main__":
    import numpy as np

    a = np.ones(44100, dtype=np.float32)
    p = apply_padding(a, 44100)
    print(f"original: {len(a)}  padded: {len(p)}  (+{len(p)-len(a)})")
