# llm/prompt/build.py
from llm.prompt.system import get_system_prompt


def build_messages(user_text: str, history: dict | None = None) -> list[dict]:
    if history:
        from llm.history.read import get_messages

        return get_messages(history)
    return [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_text},
    ]
