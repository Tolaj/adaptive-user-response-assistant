# llm/model/singleton.py
import threading
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
        from config.llm import ACTIVE_LLM_MODEL
        from llm.download.resolver import find_gguf
        from llm.model.load import load_llm

        model_dir = LLM_DIR / ACTIVE_LLM_MODEL
        if not model_dir.exists():
            raise FileNotFoundError(
                f"LLM dir not found: {model_dir}\n"
                f"Place a .gguf file at {model_dir}/"
            )
        path = find_gguf(model_dir)
        _model_path = str(path)
        _model = load_llm(path)
    return _model


def is_loaded() -> bool:
    return _model is not None


def get_model_path() -> Optional[str]:
    return _model_path
