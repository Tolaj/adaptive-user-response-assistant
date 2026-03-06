# tts/text/split.py
import re

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")

# Why 30 not 25:
# "Today's weather:" is 17 chars — was triggering a clause split and creating
# a micro-chunk. At 30 chars, clause breaks only fire on genuinely long phrases,
# keeping short conversational sentences as single chunks.
MIN_CHUNK_CHARS = 30  # was 25


def split_sentence(buf: str) -> tuple[str, str]:
    m = _SENTENCE_END.search(buf)
    if m:
        return buf[: m.end()].strip(), buf[m.end() :]
    m = _CLAUSE_BREAK.search(buf)
    if m and m.start() >= MIN_CHUNK_CHARS:
        return buf[: m.start()].strip(), buf[m.end() :]
    return "", buf
