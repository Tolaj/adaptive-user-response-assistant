import torch

WHISPER_MODEL_NAME = "base"
WHISPER_SAMPLE_RATE = 16000


def _resolve_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


WHISPER_DEVICE = _resolve_device()
print(f"[Config] Whisper device: {WHISPER_DEVICE}")
