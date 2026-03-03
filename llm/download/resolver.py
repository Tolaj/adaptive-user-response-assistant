from pathlib import Path

_PREFERENCE = ["Q4_K_M", "Q4_K_S", "Q4", "Q5_K_M", "Q5", "Q8", "q4", "q5", "q8"]


def find_gguf(model_dir: Path) -> Path:
    """Find best GGUF in model_dir, preferring Q4_K_M → Q8."""
    if not model_dir.exists():
        raise FileNotFoundError(f"Model dir not found: {model_dir}")
    gguf_files = sorted(model_dir.glob("*.gguf"))
    if not gguf_files:
        raise FileNotFoundError(f"No .gguf in {model_dir}")
    for pref in _PREFERENCE:
        for f in gguf_files:
            if pref.lower() in f.name.lower():
                return f
    return gguf_files[0]


if __name__ == "__main__":
    from config.paths import LLM_DIR
    from config.llm import ACTIVE_LLM_MODEL

    try:
        print(find_gguf(LLM_DIR / ACTIVE_LLM_MODEL))
    except FileNotFoundError as e:
        print(e)
