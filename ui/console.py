def show_partial(text: str) -> None:
    print(f"\r  \033[90m... {text:<80}\033[0m", end="", flush=True)


def show_speaking() -> None:
    print(f"\r  \033[33m● Speaking...{' ' * 60}\033[0m", flush=True)


def show_stt_final(text: str) -> None:
    print(f"\r  \033[92m✓ {text:<80}\033[0m", flush=True)


def show_you(text: str) -> None:
    print(f"\r  \033[94mYOU:\033[0m {text}")


def start_ai_line() -> None:
    print("  \033[92mAI :\033[0m ", end="", flush=True)


def prompt_you() -> None:
    print("  YOU: ", end="", flush=True)
