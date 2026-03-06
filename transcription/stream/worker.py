import threading
import time
from config.vad import TRANSCRIBE_EVERY


def start_worker(state: dict) -> None:
    state["running"] = True
    t = threading.Thread(target=_loop, args=(state,), daemon=True)
    t.start()
    state["worker_thread"] = t


def stop_worker(state: dict) -> None:
    state["running"] = False
    t = state.get("worker_thread")
    if t:
        t.join(timeout=5)
    state["worker_thread"] = None


def _loop(state: dict) -> None:
    while state["running"]:
        time.sleep(TRANSCRIBE_EVERY)
        # Don't skip — just run in a thread so the loop stays on schedule
        if state["is_transcribing"]:
            continue
        threading.Thread(target=_run_partial, args=(state,), daemon=True).start()


def _run_partial(state: dict) -> None:
    if state["is_transcribing"]:
        return
    state["is_transcribing"] = True
    try:
        from transcription.stream.partial import run_partial_pass

        text = run_partial_pass(state["buf"])
        if text and text != state["last_text"]:
            state["last_text"] = text
            state["on_partial"](text)
    finally:
        state["is_transcribing"] = False
