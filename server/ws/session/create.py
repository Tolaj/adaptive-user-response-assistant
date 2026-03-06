import threading
from config.features import ENABLE_TTS
from config.tts import (
    TTS_MODE,
    SUPERTONIC_VOICE,
    SUPERTONIC_SPEED,
    SUPERTONIC_STEPS,
    SUPERTONIC_LANGUAGE,
)
from llm.history.state import create_history
from server.logger import create_logger


def create_session() -> dict:
    """Build per-connection state dict."""
    session = {
        "history": create_history(),
        "logger": create_logger(),
        "silence_accumulated": 0,
        "in_speech": False,
        "eos_lock": threading.Lock(),
        "tts": None,
        "transcriber": None,
    }
    if ENABLE_TTS and TTS_MODE == "server":
        from tts.engine.state import create_engine
        from tts.engine.worker import start_worker

        engine = create_engine(
            voice=SUPERTONIC_VOICE,
            speed=SUPERTONIC_SPEED,
            steps=SUPERTONIC_STEPS,
            language=SUPERTONIC_LANGUAGE,
        )
        start_worker(engine)
        # added this might cause issues ----
        from tts.model.singleton import get_model as get_tts_model

        get_tts_model()
        # ----------------------------------
        session["tts"] = engine
    return session
