from config.vad import (
    NO_SPEECH_THRESHOLD,
    LOGPROB_THRESHOLD,
    COMPRESSION_RATIO_THRESHOLD,
)
from config.whisper import WHISPER_DEVICE


def build_whisper_options() -> dict:
    return {
        "language": "en",
        "fp16": (WHISPER_DEVICE == "cuda"),
        "temperature": 0,
        "condition_on_previous_text": False,
        "no_speech_threshold": NO_SPEECH_THRESHOLD,
        "compression_ratio_threshold": COMPRESSION_RATIO_THRESHOLD,
        "logprob_threshold": LOGPROB_THRESHOLD,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_whisper_options(), indent=2))
