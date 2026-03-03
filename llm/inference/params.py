# llm/inference/params.py
from config.prompt import VOICE_MAX_TOKENS, VOICE_TEMPERATURE
from llm.tools.definitions import get_tool_definitions


def build_inference_params(include_tools: bool = True) -> dict:
    params = {
        "max_tokens": VOICE_MAX_TOKENS,
        "temperature": VOICE_TEMPERATURE,
        "stream": True,
    }
    if include_tools:
        params["tools"] = get_tool_definitions()
        params["tool_choice"] = "auto"
    return params


# def build_inference_params() -> dict:
#     return {
#         "max_tokens": VOICE_MAX_TOKENS,
#         "temperature": VOICE_TEMPERATURE,
#         "stream": True,
#     }


# if __name__ == "__main__":
#     import json

#     print(json.dumps(build_inference_params(), indent=2))
