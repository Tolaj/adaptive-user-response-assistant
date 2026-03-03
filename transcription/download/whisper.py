from config.paths import WHISPER_DIR
from config.whisper import WHISPER_MODEL_NAME


def ensure_downloaded(model_name: str = WHISPER_MODEL_NAME) -> str:
    """
    Download Whisper model into models/whisper/ if missing.
    Returns path to the .pt file.
    """
    WHISPER_DIR.mkdir(parents=True, exist_ok=True)
    model_path = WHISPER_DIR / f"{model_name}.pt"
    if model_path.exists():
        print(f"[Whisper] Cached at {model_path}")
        return str(model_path)
    print(f"[Whisper] Downloading '{model_name}' → {WHISPER_DIR} ...")

    import whisper

    url = whisper._MODELS.get(model_name)
    if url is None:
        raise ValueError(
            f"Unknown model '{model_name}'. Valid: {list(whisper._MODELS)}"
        )
    whisper._download(url, str(WHISPER_DIR), in_memory=False)

    print("[Whisper] Download complete.")
    return str(model_path)


if __name__ == "__main__":
    print(ensure_downloaded())
