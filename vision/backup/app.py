import cv2
import base64
import time
from llama_cpp import Llama


from llama_cpp.llama_chat_format import Qwen3VLChatHandler

# CMAKE_ARGS="-DCMAKE_OSX_ARCHITECTURES=arm64 -DGGML_METAL=on" \
# pip install "llama-cpp-python @ git+https://github.com/JamePeng/llama-cpp-python.git" \
#   --force-reinstall --no-cache-dir


chat_handler = Qwen3VLChatHandler(
    clip_model_path="../models/vlm/qwen3vl2b/mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf"
)
llm = Llama(
    model_path="../models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf",
    chat_handler=chat_handler,
    n_ctx=1024,
    n_gpu_layers=-1,
    n_batch=512,
    n_threads=8,
    verbose=False,
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def snap_b64():
    cap.grab()
    _, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
    return base64.b64encode(buf).decode()


def query(prompt):
    img = snap_b64()
    stream = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a vision AI with access to a live camera. Answer concisely in 1-2 sentences. No lists, no numbering, no speculation. Speak naturally as if you can see the person in real time.",
            },
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
        ],
        max_tokens=60,
        temperature=0.7,
        top_p=0.8,
        top_k=20,
        repeat_penalty=1.0,  # Qwen3 uses presence_penalty instead
        stream=True,
    )
    print("\n🤖 ", end="", flush=True)
    for chunk in stream:
        delta = chunk["choices"][0]["delta"].get("content", "")
        if delta:
            print(delta, end="", flush=True)
    print("\n")


print("👁️  Commands: 'w' = watch mode, 'q' = quit, or just type a question\n")

try:
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "q":
            break

        elif user_input.lower() == "w":
            # continuous watch mode
            print("👁️  Watching... (press Ctrl+C to stop)\n")
            try:
                while True:
                    query(
                        "In one sentence, describe what the person is doing right now."
                    )
                    time.sleep(2)
            except KeyboardInterrupt:
                print("\n⏹️  Stopped watching\n")

        elif user_input:
            # ask a question
            query(user_input)

finally:
    cap.release()
