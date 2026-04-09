from pathlib import Path

_PREFERENCE = ["Q4_K_M", "Q4_K_S", "Q4", "Q5_K_M", "Q5", "Q8", "q4", "q5", "q8"]

# Maps config model name → HuggingFace repo ID
# Add new models here as needed
HF_REPOS: dict[str, str] = {
    "qwen2.5-3b": "Qwen/Qwen2.5-3B-Instruct-GGUF",
    "qwen2.5-7b": "Qwen/Qwen2.5-7B-Instruct-GGUF",
    "llama3.2-3b": "bartowski/Llama-3.2-3B-Instruct-GGUF",
    "llama3.1-8b": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    "mistral-7b": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
    "phi3.5-mini": "bartowski/Phi-3.5-mini-instruct-GGUF",
}


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
