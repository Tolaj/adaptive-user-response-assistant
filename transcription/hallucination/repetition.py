#
REPETITION_MIN_WORDS = 4
REPETITION_COUNT_THRESHOLD = 3


def has_repetition(text: str) -> bool:
    """True if the same N-word phrase repeats 3+ times (Whisper looping)."""
    words = text.lower().split()
    n = REPETITION_MIN_WORDS
    if len(words) < n * REPETITION_COUNT_THRESHOLD:
        return False
    for start in range(len(words) - n + 1):
        phrase = tuple(words[start : start + n])
        count, pos = 0, start
        while pos <= len(words) - n:
            if tuple(words[pos : pos + n]) == phrase:
                count += 1
                pos += n
            else:
                pos += 1
        if count >= REPETITION_COUNT_THRESHOLD:
            return True
    return False


if __name__ == "__main__":
    print(has_repetition("Hello how are you"))
    print(has_repetition("I want to go there. I want to go there. I want to go there."))
