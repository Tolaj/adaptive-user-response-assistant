# llm/history/clear.py
def clear_history(history: dict) -> None:
    history["turns"] = []
