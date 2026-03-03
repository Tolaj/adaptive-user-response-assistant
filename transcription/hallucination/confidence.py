# transcription/hallucination/confidence.py
from config.vad import NO_SPEECH_THRESHOLD


def passes_confidence(result: dict) -> bool:
    """True if Whisper's average no_speech_prob is below threshold."""
    segments = result.get("segments", [])
    if not segments:
        return True
    avg = sum(s.get("no_speech_prob", 0.0) for s in segments) / len(segments)
    return avg <= NO_SPEECH_THRESHOLD


if __name__ == "__main__":
    print(passes_confidence({"segments": [{"no_speech_prob": 0.9}]}))  # False
    print(passes_confidence({"segments": [{"no_speech_prob": 0.1}]}))  # True
