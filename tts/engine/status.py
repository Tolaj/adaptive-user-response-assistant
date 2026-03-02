import time


def is_speaking(engine: dict) -> bool:
    return engine["speaking"].is_set()


def wait_until_done(engine: dict, timeout: float = 2.0) -> None:
    deadline = time.time() + timeout
    time.sleep(0.05)
    while is_speaking(engine) and time.time() < deadline:
        time.sleep(0.02)


def shutdown(engine: dict) -> None:
    from tts.engine.control import interrupt

    interrupt(engine)

    from tts.engine.state import SENTINEL

    engine["queue"].put(SENTINEL)

    t = engine.get("worker_thread")
    if t:
        t.join(timeout=3)
    engine["running"] = False
