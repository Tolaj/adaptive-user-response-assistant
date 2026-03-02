import re


def clean_markdown(text: str) -> str:
    """Strip markdown symbols that would be spoken literally."""
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"_+", "", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


if __name__ == "__main__":
    print(clean_markdown("**Bold** and _italic_ with `code`"))
