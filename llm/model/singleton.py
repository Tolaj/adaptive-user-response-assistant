import threading
from pathlib import Path
from typing import Optional

_model = None
_model_path: Optional[str] = None
_lock = threading.Lock()


def get_model():
    global _model, _model_path
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model

        from config.paths import LLM_DIR
        from config.llm import ACTIVE_LLM_MODEL, LLM_REPO_ID, LLM_FILENAME
        from llm.model.load import load_llm

        model_dir = LLM_DIR / ACTIVE_LLM_MODEL
        model_dir.mkdir(exist_ok=True)  # LLM_DIR exists (paths.py), subdir may not
        gguf_path = model_dir / LLM_FILENAME

        if not gguf_path.exists():
            from llm.download.hf import download_from_hf

            download_from_hf(LLM_REPO_ID, model_dir, LLM_FILENAME)

        _model_path = str(gguf_path)
        _model = load_llm(gguf_path)
    return _model


def is_loaded() -> bool:
    return _model is not None


def get_model_path() -> Optional[str]:
    return _model_path
