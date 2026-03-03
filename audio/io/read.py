import numpy as np
import soundfile as sf


def read_wav(path: str) -> tuple[np.ndarray, int]:
    """Read a WAV file. Returns (audio_array, sample_rate)."""
    audio, sr = sf.read(path)
    return audio, sr


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "test.wav"
    audio, sr = read_wav(path)
    print(f"Loaded: shape={audio.shape}, sr={sr}, dtype={audio.dtype}")
