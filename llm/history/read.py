# llm/history/read.py
def get_messages(history: dict) -> list[dict]:
    from llm.prompt.system import get_system_prompt

    return [{"role": "system", "content": get_system_prompt()}] + history["turns"]
