import threading
import queue
import random

from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

_FILLERS = [
    "Mm-hmm.",
    "Sure.",
    "Okay.",
    "Right.",
    "Mm.",
    "Yeah.",
    "I see.",
    "Got it.",
    "Ah.",
    "Sure thing.",
]


def create_engine(
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> dict:
    """Create TTS engine state dict. Call start_worker(engine) to begin."""
    return {
        "voice": voice,
        "speed": speed,
        "steps": steps,
        "language": language,
        "token_buf": "",
        "queue": queue.PriorityQueue(),
        "interrupted": threading.Event(),
        "speaking": threading.Event(),
        "running": False,
        "worker_thread": None,
        "fillers": _FILLERS,
    }


SENTINEL = (float("inf"), None)  # sorts last, always
