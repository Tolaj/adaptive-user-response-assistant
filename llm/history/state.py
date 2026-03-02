from config.prompt import VOICE_MAX_HISTORY_TURNS


def create_history(max_turns: int = VOICE_MAX_HISTORY_TURNS) -> dict:
    return {"turns": [], "max_turns": max_turns}
