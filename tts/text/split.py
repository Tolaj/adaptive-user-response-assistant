import re

_SENTENCE_END = re.compile(r"(?<![A-Z][a-z])(?<!\d)([.?!])(\s+|$)")
_CLAUSE_BREAK = re.compile(r"[,;:]\s+")
MIN_CHUNK_CHARS = 6


def split_sentence(buf: str) -> tuple[str, str]:
    """Split buf at first sentence/clause boundary. Returns (chunk, remainder)."""
    m = _SENTENCE_END.search(buf)
    if m:
        return buf[: m.end()].strip(), buf[m.end() :]
    m = _CLAUSE_BREAK.search(buf)
    if m and m.start() >= MIN_CHUNK_CHARS:
        return buf[: m.start()].strip(), buf[m.end() :]
    return "", buf


if __name__ == "__main__":
    print(split_sentence("Hello world. This is a test."))
    print(split_sentence("Waiting, for more"))
