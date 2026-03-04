# audio/transform/denoise.py
import numpy as np


def denoise(
    audio: np.ndarray, noise_profile: np.ndarray, sr: int = 16000
) -> np.ndarray:
    """
    Reduce noise in audio using a noise profile sample.
    noise_profile: a short clip of background noise (from preroll).
    Returns cleaned float32 array same length as audio.
    """
    try:
        import noisereduce as nr

        return nr.reduce_noise(
            y=audio.astype(np.float32),
            sr=sr,
            y_noise=noise_profile.astype(np.float32),
            stationary=False,
            prop_decrease=0.8,  # 0.8 = aggressive but keeps speech natural
        ).astype(np.float32)
    except Exception as e:
        print(f"[Denoise] {e}")
        return audio
