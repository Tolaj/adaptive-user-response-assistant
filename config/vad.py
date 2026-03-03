RECORD_SAMPLE_RATE = 44100
PREROLL_SECONDS = 0.25
SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 1.2
MIN_SPEECH = 0.45
ROLLING_WINDOW_SEC = 8.0

ENERGY_THRESHOLD = (
    0.015  # Increased: rejects background music, needs stronger signal for speech
)
MIN_SPEECH_SEC = (
    0.40  # Increased: requires longer speech burst (music pauses are short)
)
PAUSE_SECONDS = 1.2

MIN_AUDIO_SEC = 0.40
NO_SPEECH_THRESHOLD = (
    0.60  # Increased: Whisper requires higher confidence (rejects music hallucinations)
)
LOGPROB_THRESHOLD = (
    1.0  # Increased (less negative): stricter confidence for transcription acceptance
)
TRANSCRIBE_EVERY = 0.4
COMPRESSION_RATIO_THRESHOLD = (
    2.0  # Lowered: more aggressive at rejecting repetitive content (music)
)
