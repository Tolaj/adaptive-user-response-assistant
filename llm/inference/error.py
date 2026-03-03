# llm/inference/error.py
def handle_inference_error(e: Exception) -> str:
    msg = f"[LLM error: {e}]"
    print(msg)
    return msg
