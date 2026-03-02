import numpy as np
from config.vad import SILENCE_THRESHOLD
from config.whisper import WHISPER_SAMPLE_RATE

from config.vad import SILENCE_DURATION

_SILENCE_SAMPLES = int(SILENCE_DURATION * WHISPER_SAMPLE_RATE)


def handle_audio_frame(data: bytes, session: dict, trigger_eos_fn) -> None:
    if not session.get("transcriber"):
        return
    tts = session.get("tts")
    if tts:
        from tts.engine.status import is_speaking

        if is_speaking(tts):
            session["silence_accumulated"] = 0
            session["in_speech"] = False
            return
    chunk = np.frombuffer(data, dtype=np.float32)
    from transcription.stream import feed

    feed(session["transcriber"], chunk)
    amp = float(np.abs(chunk).mean())
    if amp > SILENCE_THRESHOLD:
        session["in_speech"] = True
        session["silence_accumulated"] = 0
    elif session["in_speech"]:
        session["silence_accumulated"] += len(chunk)
        if session["silence_accumulated"] >= _SILENCE_SAMPLES:
            trigger_eos_fn()
