# transcription/stream/__init__.py
from stt.stream.buffer import create_buffer
from stt.stream.worker import start_worker, stop_worker
from stt.stream.final import run_final_pass


def create_stream(on_partial, on_final, sample_rate: int = 16000) -> dict:
    return {
        "buf": create_buffer(sample_rate),
        "on_partial": on_partial,
        "on_final": on_final,
        "last_text": "",
        "last_partial_samples": 0,  # add this
        "running": False,
        "worker_thread": None,
        "is_transcribing": False,
    }


def start_stream(state: dict) -> None:
    start_worker(state)


def stop_stream(state: dict) -> None:
    stop_worker(state)


def feed(state: dict, chunk) -> None:
    from stt.stream.buffer import append

    append(state["buf"], chunk)


def end_of_speech(state: dict) -> str:
    text = run_final_pass(state["buf"])
    state["last_text"] = ""
    if text:
        state["on_final"](text)
    return text


def clear_stream(state: dict) -> None:
    from stt.stream.buffer import clear_buffer

    clear_buffer(state["buf"])
    state["last_text"] = ""
