# llm/history/trim.py
def trim_history(history: dict) -> None:
    limit = history["max_turns"] * 2
    if len(history["turns"]) > limit:
        history["turns"] = history["turns"][-limit:]
