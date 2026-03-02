from typing import Generator

from llm.model.singleton import get_model
from llm.history.add import add_user, add_assistant
from llm.prompt.build import build_messages
from llm.inference.params import build_inference_params
from llm.inference.error import handle_inference_error


def stream_response(
    user_text: str,
    history: dict | None = None,
) -> Generator[str, None, None]:
    """Yield tokens one by one. Logs exchange to history if provided."""
    llm = get_model()
    if history:
        add_user(history, user_text)
    messages = build_messages(user_text, history)
    params = build_inference_params()
    full = ""
    try:
        for chunk in llm.create_chat_completion(messages=messages, **params):
            token = chunk["choices"][0]["delta"].get("content", "")
            if token:
                full += token
                yield token
    except Exception as e:
        err = handle_inference_error(e)
        yield err
        full = err
    if history and full:
        add_assistant(history, full)


if __name__ == "__main__":
    from llm.history.state import create_history

    h = create_history()
    print("Response: ", end="", flush=True)
    for tok in stream_response("Hello, who are you?", h):
        print(tok, end="", flush=True)
    print()
