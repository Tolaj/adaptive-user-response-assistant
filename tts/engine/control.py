import random


def interrupt(engine: dict) -> None:
    """Stop playback and drain pending queue."""
    engine["interrupted"].set()
    _drain(engine)
    from tts.playback.stop import stop_audio

    stop_audio()


def resume(engine: dict) -> None:
    """Clear interrupted flag before next feed_token()."""
    engine["token_buf"] = ""
    engine["interrupted"].clear()


def speak_filler(engine: dict) -> None:
    """Enqueue a random filler at priority 0 (plays immediately)."""
    from tts.engine.queue import enqueue

    enqueue(engine, random.choice(engine["fillers"]), priority=0)


def _drain(engine: dict) -> None:
    while not engine["queue"].empty():
        try:
            engine["queue"].get_nowait()
        except Exception:
            break
