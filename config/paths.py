from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
WHISPER_DIR = MODELS_DIR / "whisper"
LLM_DIR = MODELS_DIR / "llm"
SUPERTONIC_DIR = MODELS_DIR / "supertonic"

for _d in (LOGS_DIR, MODELS_DIR, WHISPER_DIR, LLM_DIR, SUPERTONIC_DIR):
    _d.mkdir(parents=True, exist_ok=True)
