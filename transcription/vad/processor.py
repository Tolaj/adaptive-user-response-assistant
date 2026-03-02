import numpy as np
from config.vad import PAUSE_SECONDS, MIN_SPEECH_SEC
from transcription.vad.state import reset_vad_state
from transcription.vad.energy import is_speech_energy


def process_chunk(
    chunk: np.ndarray,
    state: dict,
    on_speech_start=None,
    on_speech_end=None,
) -> None:
    pause_samples = int(PAUSE_SECONDS * state["sample_rate"])
    min_samples = int(MIN_SPEECH_SEC * state["sample_rate"])
    is_speech = is_speech_energy(chunk)

    if is_speech:
        if not state["in_speech"]:
            state["in_speech"] = True
            state["silence_count"] = 0
            if on_speech_start:
                on_speech_start()
        state["speech_samples"] += len(chunk)
        state["silence_count"] = 0
    elif state["in_speech"]:
        state["silence_count"] += len(chunk)
        state["speech_samples"] += len(chunk)
        if state["silence_count"] >= pause_samples:
            if state["speech_samples"] >= min_samples and on_speech_end:
                on_speech_end()
            reset_vad_state(state)


if __name__ == "__main__":
    import numpy as np

    from transcription.vad.state import create_vad_state

    s = create_vad_state()
    for _ in range(20):
        process_chunk(
            np.random.randn(1600).astype(np.float32) * 0.5,
            s,
            lambda: print("START"),
            lambda: print("END"),
        )
    for _ in range(60):
        process_chunk(
            np.zeros(1600, dtype=np.float32),
            s,
            lambda: print("START"),
            lambda: print("END"),
        )

    for _ in range(20):
        process_chunk(
            np.random.randn(1600).astype(np.float32) * 0.5,
            s,
            lambda: print("START"),
            lambda: print("END"),
        )
    for _ in range(60):
        process_chunk(
            np.zeros(1600, dtype=np.float32),
            s,
            lambda: print("START"),
            lambda: print("END"),
        )
