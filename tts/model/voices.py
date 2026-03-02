import os
import numpy as np

VALID_VOICES = ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"]
STYLE_DIM = 128


def load_style(voice: str, model_path: str) -> np.ndarray:
    """Load voice style embedding → shape (1, N, 128)."""
    if voice not in VALID_VOICES:
        raise ValueError(f"Voice '{voice}' invalid. Choose from: {VALID_VOICES}")
    path = os.path.join(model_path, "voices", f"{voice}.bin")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Voice file not found: {path}")
    return np.fromfile(path, dtype=np.float32).reshape(1, -1, STYLE_DIM)


if __name__ == "__main__":
    from tts.model.singleton import get_model

    m = get_model()
    print(load_style("F1", m["model_path"]).shape)
