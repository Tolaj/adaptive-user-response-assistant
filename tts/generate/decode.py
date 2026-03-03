import numpy as np


def decode_waveform(latents: np.ndarray, model: dict) -> np.ndarray:
    """Decode latents → raw waveform via voice_decoder."""
    return model["voice_decoder"].run(None, {"latents": latents})[0]
