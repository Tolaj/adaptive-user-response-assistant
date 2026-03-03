from config.prompt import VOICE_MAX_TOKENS, VOICE_TEMPERATURE


def build_inference_params() -> dict:
    return {
        "max_tokens": VOICE_MAX_TOKENS,
        "temperature": VOICE_TEMPERATURE,
        "stream": True,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_inference_params(), indent=2))
