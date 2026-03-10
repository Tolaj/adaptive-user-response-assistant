# config/vad.py
RECORD_SAMPLE_RATE = 44100
PREROLL_SECONDS = 0.25
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 0.6
MIN_SPEECH = 0.3
ROLLING_WINDOW_SEC = 8.0

ENERGY_THRESHOLD = (
    0.025  # Increased: rejects background music, needs stronger signal for speech
)
MIN_SPEECH_SEC = (
    0.25  # Increased: requires longer speech burst (music pauses are short)
)
PAUSE_SECONDS = 0.65

MIN_AUDIO_SEC = 0.30
NO_SPEECH_THRESHOLD = (
    0.45  # Increased: Whisper requires higher confidence (rejects music hallucinations)
)
LOGPROB_THRESHOLD = (
    -0.8  # Increased (less negative): stricter confidence for transcription acceptance
)
TRANSCRIBE_EVERY = 0.8
COMPRESSION_RATIO_THRESHOLD = (
    2.0  # Lowered: more aggressive at rejecting repetitive content (music)
)

SILERO_THRESHOLD = 0.45  # was 0.5 — only triggers on high-confidence speech

DENOISE_ENABLED = False
PUSH_TO_TALK = False

WAKE_WORD = "follow"
WAKE_WORD_ENABLED = True
SLEEP_WORD = "sleep"
