# tts/engine/state.py
import threading
import queue
import itertools

from config.tts import (
    SUPERTONIC_VOICE,
    SUPERTONIC_LANGUAGE,
    SUPERTONIC_STEPS,
    SUPERTONIC_SPEED,
)

# Filler range designed to cover the observed LLM first-token distribution:
#   min observed: 1287ms  max observed: 2189ms  avg: 1728ms
# We need fillers from ~1300ms to ~2200ms so adaptive selection can always
# find one that lands just above the current rolling estimate.
_FILLERS = [
    "Got it.",  # ~700ms  — short fallback
    "Sure.",  # ~650ms  — short fallback
    "Okay.",  # ~680ms  — short fallback
    "Sure thing.",  # ~1050ms
    "Right, on it.",  # ~1200ms
    "Sure, let me check.",  # ~1500ms
    "Okay, one moment.",  # ~1550ms
    "Let me look at that.",  # ~1700ms
    "Sure, one moment please.",  # ~1850ms
    "Okay, let me check that.",  # ~1900ms
    "Sure, give me just a moment.",  # ~2100ms
]

SENTINEL = (float("inf"), float("inf"), None)


def create_engine(
    voice: str = SUPERTONIC_VOICE,
    speed: float = SUPERTONIC_SPEED,
    steps: int = SUPERTONIC_STEPS,
    language: str = SUPERTONIC_LANGUAGE,
) -> dict:
    return {
        "voice": voice,
        "speed": speed,
        "steps": steps,
        "language": language,
        "token_buf": "",
        "queue": queue.PriorityQueue(),
        "seq": itertools.count(),
        "interrupted": threading.Event(),
        "speaking": threading.Event(),
        "running": False,
        "worker_thread": None,
        "fillers": _FILLERS,
        "filler_audio": {},  # text → np.ndarray
        "filler_durations_ms": {},  # text → float ms (measured at warmup)
        # Rolling EMA of LLM first-token latency — used by speak_filler()
        # to pick a filler that covers the gap. Seeded at 1800ms (slightly
        # above the 1728ms avg) so first response is covered conservatively.
        "last_llm_first_token_ms": 1800.0,
    }


def warm_fillers(engine: dict) -> None:
    """Pre-generate all filler audio and record exact durations."""
    from tts.generate.pipeline import generate_one
    from tts.model.singleton import get_model

    sr = get_model()["sample_rate"]
    print("[TTS] Pre-generating fillers...")
    for text in _FILLERS:
        try:
            audio = generate_one(
                text,
                voice=engine["voice"],
                speed=engine["speed"],
                steps=engine["steps"],
                language=engine["language"],
            )
            engine["filler_audio"][text] = audio
            engine["filler_durations_ms"][text] = len(audio) / sr * 1000
        except Exception as e:
            print(f"[TTS] Filler warmup failed for '{text}': {e}")

    dur = engine["filler_durations_ms"]
    print(
        f"[TTS] {len(engine['filler_audio'])} fillers ready  "
        f"range: {min(dur.values()):.0f}–{max(dur.values()):.0f}ms"
    )
