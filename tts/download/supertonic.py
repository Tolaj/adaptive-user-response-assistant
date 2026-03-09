import warnings
from config.paths import SUPERTONIC_DIR

MODEL_ID = "onnx-community/Supertonic-TTS-2-ONNX"

_REQUIRED_FILES = [
    "onnx/text_encoder.onnx",
    "onnx/text_encoder.onnx_data",
    "onnx/latent_denoiser.onnx",
    "onnx/latent_denoiser.onnx_data",
    "onnx/voice_decoder.onnx",
    "onnx/voice_decoder.onnx_data",
    "tokenizer.json",
]


def ensure_downloaded() -> str:
    missing = [f for f in _REQUIRED_FILES if not (SUPERTONIC_DIR / f).exists()]
    
    if not missing:
        return str(SUPERTONIC_DIR)
    
    print(f"[Supertonic] Missing files: {missing}")
    print(f"[Supertonic] Downloading {MODEL_ID} → {SUPERTONIC_DIR}")
    print("[Supertonic] (one-time ~200 MB download)")
    
    from huggingface_hub import snapshot_download
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        snapshot_download(repo_id=MODEL_ID, local_dir=str(SUPERTONIC_DIR))
    
    # verify all files are now present
    still_missing = [f for f in _REQUIRED_FILES if not (SUPERTONIC_DIR / f).exists()]
    if still_missing:
        raise RuntimeError(f"[Supertonic] Download incomplete, still missing: {still_missing}")
    
    print("[Supertonic] Download complete.")
    return str(SUPERTONIC_DIR)


if __name__ == "__main__":
    print(ensure_downloaded())