# tts/engine/feed.py
from tts.text.split import split_sentence, MIN_CHUNK_CHARS
from tts.engine.queue import enqueue
from config.tts import WORD_FLUSH_THRESHOLD, MIN_SEND_CHARS as _MIN_SEND_CHARS


def feed_token(engine: dict, token: str) -> None:
    if engine["interrupted"].is_set():
        return
    engine["token_buf"] += token

    # Sentence/clause boundary split
    while True:
        sentence, remainder = split_sentence(engine["token_buf"])
        if sentence and len(sentence) >= _MIN_SEND_CHARS:
            engine["token_buf"] = remainder
            enqueue(engine, sentence, priority=1)
        else:
            break

    # Word-count flush
    if len(engine["token_buf"].split()) >= WORD_FLUSH_THRESHOLD:
        text = engine["token_buf"].strip()
        engine["token_buf"] = ""
        if text:
            enqueue(engine, text, priority=1)


def flush(engine: dict) -> None:
    """
    Called after LLM finishes streaming.

    The [6, 1] trailing chunk problem:
      LLM outputs "Check latest air news sites for updates."
      Word-flush fires at "Check latest air news sites for" (6 words) → chunk 1
      Remainder: "updates." → 1 word, has terminal punct → was sent as chunk 2

    Fix: append the short tail onto the PREVIOUS chunk that's already queued,
    rather than sending it standalone. We do this by peeking at what's in the
    queue and merging if the last item is recent and short tail qualifies.

    If queue is empty (whole response fit in one flush), just send normally.

    Minimum standalone flush = 4 words OR the buffer is the entire response
    (i.e. nothing was enqueued yet during feed_token — short responses).
    """
    text = engine["token_buf"].strip()
    engine["token_buf"] = ""

    if not text:
        return

    words = text.split()

    # Short tail (< 4 words) — try to merge with last queued chunk instead
    if len(words) < 4:
        merged = _try_merge_with_last(engine, text)
        if merged:
            return  # successfully appended to previous chunk

    # Either long enough to stand alone, or nothing in queue to merge with
    enqueue(engine, text, priority=1)


def _try_merge_with_last(engine: dict, tail: str) -> bool:
    """
    Pop the last item from the priority queue, append tail, re-enqueue.
    Returns True if merge succeeded, False if queue was empty or wrong type.

    PriorityQueue doesn't support peek/pop-last, so we drain into a list,
    modify the last item, and re-fill. This is safe because flush() is called
    after the LLM loop ends — no concurrent feed_token() calls at this point.
    """
    q = engine["queue"]
    items = []
    while not q.empty():
        try:
            items.append(q.get_nowait())
        except Exception:
            break

    if not items:
        return False

    # Find the last normal-priority item (priority=1)
    last_idx = None
    for i in range(len(items) - 1, -1, -1):
        if items[i][0] == 1:  # normal priority
            last_idx = i
            break

    if last_idx is None:
        # Only filler items in queue — put everything back, send tail standalone
        for item in items:
            q.put(item)
        return False

    # Merge tail onto the last chunk
    priority, seq, prev_text = items[last_idx]
    merged_text = (prev_text.rstrip(".!?,;:") + " " + tail).strip()
    items[last_idx] = (priority, seq, merged_text)

    for item in items:
        q.put(item)

    return True
