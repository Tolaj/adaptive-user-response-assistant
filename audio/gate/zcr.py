import numpy as np


def zero_crossing_rate(audio: np.ndarray) -> float:
    """Fraction of samples where sign changes."""
    if len(audio) <= 1:
        return 0.0
    return float(np.mean(np.abs(np.diff(np.sign(audio.astype(np.float32)))) / 2))


if __name__ == "__main__":
    import numpy as np

    tone = np.sin(np.linspace(0, 2 * np.pi * 10, 1000)).astype(np.float32)
    noise = np.random.randn(1000).astype(np.float32)
    print(
        f"tone ZCR: {zero_crossing_rate(tone):.4f}  noise ZCR: {zero_crossing_rate(noise):.4f}"
    )
