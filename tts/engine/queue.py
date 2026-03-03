def enqueue(engine: dict, text: str, priority: int = 1) -> None:
    """priority=0 → filler (plays first), priority=1 → normal."""
    seq = next(engine["seq"])
    engine["queue"].put((priority, seq, text))
