# config/features.py
# ── Mode selector ─────────────────────────────────────────────
# Pick ONE mode:
#   "server"                → Flask + WebSocket server only
#   "stt_only"              → Mic → Whisper, print transcript
#   "tts_only"              → Type text → speak it aloud
#   "text_to_text_chat"     → Type text → LLM → print response (no audio)
#   "voice_to_text_chat"    → Mic → Whisper → LLM → print response (no TTS)
#   "full"                  → Mic → Whisper → LLM → TTS (everything)

MODE = "voice_screen"

# ── Derived flags (do not edit) ───────────────────────────────
ENABLE_STT = MODE in ("tts_only", "voice_to_text_chat", "full")
ENABLE_TTS = MODE in ("tts_only", "full")
ENABLE_LLM = MODE in ("text_to_text_chat", "voice_to_text_chat", "full", "tts_only")
ENABLE_SERVER = MODE == "server"
ENABLE_VISION = MODE in ("vision_text", "vision_speech", "voice_screen")
SHOW_TEXT = True
