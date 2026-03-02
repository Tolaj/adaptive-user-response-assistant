from tts.text.split import split_sentence, MIN_CHUNK_CHARS
from tts.engine.queue import enqueue

WORD_FLUSH_THRESHOLD = 8


def feed_token(engine: dict, token: str) -> None:
    """Accumulate token; push complete sentences/clauses to queue."""
    if engine["interrupted"].is_set():
        return
    engine["token_buf"] += token
    while True:
        sentence, remainder = split_sentence(engine["token_buf"])
        if sentence and len(sentence) >= MIN_CHUNK_CHARS:
            engine["token_buf"] = remainder
            enqueue(engine, sentence, priority=1)
        else:
            break
    if len(engine["token_buf"].split()) >= WORD_FLUSH_THRESHOLD:
        text = engine["token_buf"].strip()
        engine["token_buf"] = ""
        if text:
            enqueue(engine, text, priority=1)


def flush(engine: dict) -> None:
    """Push any remaining buffer."""
    text = engine["token_buf"].strip()
    engine["token_buf"] = ""
    if text and len(text) >= 2:
        enqueue(engine, text, priority=1)
