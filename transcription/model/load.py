# transcription/model/load.py
import torch
import whisper
import whisper.model as wm

from config.paths import WHISPER_DIR
from config.whisper import WHISPER_MODEL_NAME
from transcription.model.device import resolve_device


def load_whisper(
    model_name: str = WHISPER_MODEL_NAME,
    device: str | None = None,
) -> wm.Whisper:
    """Load Whisper from models/whisper/. Downloads if missing."""
    from transcription.download.whisper import ensure_downloaded

    if device is None:
        device = resolve_device()
    ensure_downloaded(model_name)
    model_path = WHISPER_DIR / f"{model_name}.pt"
    print(f"[Whisper] Loading '{model_name}' on {device} ...")
    checkpoint = torch.load(str(model_path), map_location="cpu")
    dims = wm.ModelDimensions(**checkpoint["dims"])
    model = wm.Whisper(dims)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)

    # warm up Metal kernels — kills the 5s cold-start on first real call
    print("[Whisper] Warming up...")
    import whisper as _w
    import numpy as np

    # 480000 = 30s at 16kHz — Whisper's full window
    # pre-compiles the Metal kernel for the largest possible input
    _w.transcribe(
        model,
        np.zeros(480000, dtype=np.float32),
        language="en",
        fp16=(device == "cuda"),
    )
    print(f"[Whisper] Ready on {device}.")
    return model


if __name__ == "__main__":
    m = load_whisper()
    print(type(m))
