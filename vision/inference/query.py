from config.vlm import (
    VLM_BACKEND,
    VLM_SYSTEM_PROMPT,
    VLM_MAX_TOKENS,
    VLM_TEMPERATURE,
    VLM_TOP_P,
    VLM_TOP_K,
    VLM_PRESENCE_PENALTY,
    VLM_SERVER_PORT,
)
from vision.inference.snap import snap_b64


def query_stream(prompt: str):
    img = snap_b64()
    messages = [
        {"role": "system", "content": VLM_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img}"},
                },
                {"type": "text", "text": prompt},
            ],
        },
    ]
    params = dict(
        max_tokens=VLM_MAX_TOKENS,
        temperature=VLM_TEMPERATURE,
        top_p=VLM_TOP_P,
        top_k=VLM_TOP_K,
        presence_penalty=VLM_PRESENCE_PENALTY,
        stream=True,
    )

    if VLM_BACKEND == "package":
        yield from _query_package(messages, params)
    else:
        yield from _query_server(messages, params)


def _query_package(messages, params):
    from vision.model.singleton import get_model

    llm = get_model()
    for chunk in llm.create_chat_completion(messages=messages, **params):
        token = chunk["choices"][0]["delta"].get("content", "")
        if token:
            yield token


def _query_server(messages, params):
    import json
    import requests

    params.pop("top_k", None)  # openai API doesn't support top_k
    response = requests.post(
        f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
        json={"messages": messages, **params},
        stream=True,
        timeout=30,
    )
    for line in response.iter_lines():
        if line and line != b"data: [DONE]":
            try:
                chunk = json.loads(line.decode().replace("data: ", ""))
                token = chunk["choices"][0]["delta"].get("content", "")
                if token:
                    yield token
            except:
                pass
