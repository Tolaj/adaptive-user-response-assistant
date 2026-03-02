def normalise_text(text: str) -> str:
    """Ensure terminal punctuation; add prosody lead-in for short inputs."""
    text = text.strip()
    if not text:
        return text
    if text[-1] not in ".!?,;:":
        text += "."
    if len(text.split()) <= 3:
        text = ", " + text
    return text


if __name__ == "__main__":
    for t in ["Hello", "How are you", "Already a sentence."]:
        print(f"'{t}' → '{normalise_text(t)}'")
