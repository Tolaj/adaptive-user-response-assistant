# llm/inference/stream.py
# from typing import Generator

# from llm.model.singleton import get_model
# from llm.history.add import add_user, add_assistant
# from llm.prompt.build import build_messages
# from llm.inference.params import build_inference_params
# from llm.inference.error import handle_inference_error


# def stream_response(
#     user_text: str,
#     history: dict | None = None,
# ) -> Generator[str, None, None]:
#     """Yield tokens one by one. Logs exchange to history if provided."""
#     llm = get_model()
#     if history:
#         add_user(history, user_text)
#     messages = build_messages(user_text, history)
#     params = build_inference_params()
#     full = ""
#     try:
#         for chunk in llm.create_chat_completion(messages=messages, **params):
#             token = chunk["choices"][0]["delta"].get("content", "")
#             if token:
#                 full += token
#                 yield token
#     except Exception as e:
#         err = handle_inference_error(e)
#         yield err
#         full = err
#     if history and full:
#         add_assistant(history, full)


# if __name__ == "__main__":
#     from llm.history.state import create_history

#     h = create_history()
#     print("Response: ", end="", flush=True)
#     for tok in stream_response("Hello, who are you?", h):
#         print(tok, end="", flush=True)
#     print()


import json
from typing import Generator

from llm.model.singleton import get_model
from llm.history.add import add_user, add_assistant, add_tool_call, add_tool_result
from llm.prompt.build import build_messages
from llm.inference.params import build_inference_params
from llm.inference.error import handle_inference_error


def stream_response(
    user_text: str,
    history: dict | None = None,
) -> Generator[str, None, None]:

    params = build_inference_params(include_tools=True)

    llm = get_model()
    if history:
        add_user(history, user_text)
    messages = build_messages(user_text, history)
    params = build_inference_params(include_tools=True)
    for token in _run(llm, messages, params, history):
        yield token


def _run(llm, messages, params, history):
    full_text = ""
    in_tool_block = False
    tool_buf = ""

    try:

        for chunk in llm.create_chat_completion(messages=messages, **params):
            choice = chunk["choices"][0]
            if not isinstance(choice, dict):
                continue
            delta = choice.get("delta", {})
            if not isinstance(delta, dict):
                continue

            token = delta.get("content", "")
            if not isinstance(token, str) or not token:  # change this line
                continue

            full_text += token

            # detect start of tool call block
            if "<tool_call>" in full_text and not in_tool_block:
                in_tool_block = True

            if in_tool_block:
                tool_buf += token
                if "</tool_call>" in tool_buf:
                    # extract JSON between tags
                    inner = (
                        tool_buf.split("<tool_call>")[-1]
                        .split("</tool_call>")[0]
                        .strip()
                    )
                    yield " "  # heartbeat for TTS
                    result = _parse_and_execute(inner)

                    tool_call_id = "tc_0"
                    try:
                        clean = inner.replace("{{", "{").replace("}}", "}")
                        parsed = json.loads(clean)
                        name = parsed.get("name", "")
                        arguments = json.dumps(parsed.get("arguments", {}))
                    except Exception:
                        name, arguments = "unknown", "{}"
                    if history:
                        add_tool_call(history, tool_call_id, name, arguments)
                        add_tool_result(history, tool_call_id, result)
                        followup_messages = build_messages("", history)
                    else:
                        followup_messages = messages + [
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "content": result,
                            }
                        ]
                    params2 = build_inference_params(include_tools=False)
                    for t in _run(llm, followup_messages, params2, None):
                        yield t
                    return
                # don't yield tool call text to TTS
                continue

            yield token

    except Exception as e:
        err = handle_inference_error(e)
        yield err
        full_text = err

    if history and full_text and not in_tool_block:
        add_assistant(history, full_text)


def _parse_and_execute(inner: str) -> str:
    import json

    try:
        clean = inner.replace("{{", "{").replace("}}", "}")
        parsed = json.loads(clean)
        name = parsed.get("name", "")
        args = parsed.get("arguments", {})
    except Exception as e:
        return f"[Tool parse error] {e}"
    from llm.tools.executor import execute

    return execute(name, args)


def _execute(name: str, args_json: str) -> str:
    try:
        args = json.loads(args_json) if args_json else {}
    except Exception:
        args = {}
    from llm.tools.executor import execute

    return execute(name, args)
