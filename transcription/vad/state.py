def create_vad_state(sample_rate: int = 16000) -> dict:
    return {
        "sample_rate": sample_rate,
        "in_speech": False,
        "silence_count": 0,
        "speech_samples": 0,
    }


def reset_vad_state(state: dict) -> None:
    state["in_speech"] = False
    state["silence_count"] = 0
    state["speech_samples"] = 0
