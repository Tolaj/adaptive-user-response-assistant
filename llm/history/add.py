# llm/history/add.py
from llm.history.trim import trim_history


def add_user(history: dict, text: str) -> None:
    history["turns"].append({"role": "user", "content": text})
    trim_history(history)


def add_assistant(history: dict, text: str) -> None:
    history["turns"].append({"role": "assistant", "content": text})
    trim_history(history)


# def add_tool_call(history: dict, tool_call_id: str, name: str, arguments: str) -> None:
#     history["turns"].append(
#         {
#             "role": "assistant",
#             "content": None,
#             "tool_calls": [
#                 {
#                     "id": tool_call_id,
#                     "type": "function",
#                     "function": {"name": name, "arguments": arguments},
#                 }
#             ],
#         }
#     )


def add_tool_call(history: dict, tool_call_id: str, name: str, arguments: str) -> None:
    history["turns"].append(
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_call_id,
                    "type": "function",
                    "function": {"name": name, "arguments": arguments},
                }
            ],
        }
    )


def add_tool_result(history: dict, tool_call_id: str, content: str) -> None:
    history["turns"].append(
        {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content,
        }
    )
