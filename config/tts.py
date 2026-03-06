# config/tts.py
TTS_MODE = "server"
TTS_SERVER_BACKEND = "supertonic2"

SUPERTONIC_VOICE = "F1"
SUPERTONIC_LANGUAGE = "en"
SUPERTONIC_STEPS = 10  # was 15 → benchmark: 685ms first chunk avg
SUPERTONIC_SPEED = 1
ENABLE_FILLER = False

# Speech smoothness — how text is chunked before TTS generation
# Higher WORD_FLUSH_THRESHOLD = fewer, longer chunks = smoother but slightly more latency
# Lower  WORD_FLUSH_THRESHOLD = more, shorter chunks = faster first word but choppier
WORD_FLUSH_THRESHOLD = 10  # words buffered before a mid-sentence force-flush

# Minimum chars a sentence-split piece must be before it's sent standalone
# Lower = more splits (choppier), Higher = fewer splits (smoother)
MIN_SEND_CHARS = 35

# How long the worker waits to merge back-to-back chunks into one generation call
# Higher = smoother (fewer ONNX calls), but adds that many ms of latency per chunk
MERGE_WINDOW_SEC = 0.04
