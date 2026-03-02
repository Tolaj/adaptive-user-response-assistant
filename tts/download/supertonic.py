import warnings
from config.paths import SUPERTONIC_DIR

MODEL_ID = "onnx-community/Supertonic-TTS-2-ONNX"


def ensure_downloaded() -> str:
    """Download Supertonic 2 ONNX into models/supertonic/ if missing."""
    marker = SUPERTONIC_DIR / "onnx" / "text_encoder.onnx"
    if marker.exists():
        return str(SUPERTONIC_DIR)
    print(f"[Supertonic] Downloading {MODEL_ID} → {SUPERTONIC_DIR}")
    print("[Supertonic] (one-time ~200 MB download)")
    from huggingface_hub import snapshot_download

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=MODEL_ID, local_dir=str(SUPERTONIC_DIR))
    print("[Supertonic] Download complete.")
    return str(SUPERTONIC_DIR)


if __name__ == "__main__":
    print(ensure_downloaded())
