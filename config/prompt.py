# config/prompt.py
VOICE_SYSTEM_PROMPT = (
    "You are a concise voice assistant. " "Never use lists or markdown."
)
VOICE_MAX_TOKENS = 60  # was 150 — prevents long multi-chunk responses
VOICE_TEMPERATURE = 0.7
VOICE_MAX_HISTORY_TURNS = 10
