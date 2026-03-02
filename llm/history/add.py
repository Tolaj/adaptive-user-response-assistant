from llm.history.trim import trim_history


def add_user(history: dict, text: str) -> None:
    history["turns"].append({"role": "user", "content": text})
    trim_history(history)


def add_assistant(history: dict, text: str) -> None:
    history["turns"].append({"role": "assistant", "content": text})
    trim_history(history)
