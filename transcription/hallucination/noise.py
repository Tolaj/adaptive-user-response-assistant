import re

_PATTERNS = [
    re.compile(r"^\[.*\]$", re.IGNORECASE),
    re.compile(r"^\(.*\)$", re.IGNORECASE),
    re.compile(r"^[\s\.\,\!\?]*$"),
]


def is_noise_phrase(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    return any(p.match(t) for p in _PATTERNS)


def clean_text(text: str) -> str:
    t = text.strip()
    return "" if is_noise_phrase(t) else t


if __name__ == "__main__":
    for t in ["[BLANK_AUDIO]", "Hello world", "...", "(music)"]:
        print(f"'{t}' → noise={is_noise_phrase(t)}")
