from config.prompt import VOICE_SYSTEM_PROMPT


def get_system_prompt() -> str:
    return VOICE_SYSTEM_PROMPT


if __name__ == "__main__":
    print(get_system_prompt())
