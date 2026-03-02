import numpy as np
import soundfile as sf


def write_wav(audio: np.ndarray, path: str, sample_rate: int) -> str:
    """Write numpy array to WAV. Returns path."""
    sf.write(path, audio, sample_rate)
    return path


if __name__ == "__main__":
    import numpy as np

    audio = np.zeros(16000, dtype=np.float32)
    print(write_wav(audio, "/tmp/test_out.wav", 16000))
