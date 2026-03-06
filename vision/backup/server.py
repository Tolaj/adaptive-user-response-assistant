import cv2
import base64
import json
import requests
import subprocess
import time

# Start llama-server
server = subprocess.Popen(
    [
        "llama-server",
        "-m",
        "../models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf",
        "--mmproj",
        "../models/vlm/qwen3vl2b/mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf",
        "-ngl",
        "99",
        "-c",
        "2048",
        "--port",
        "8080",
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

# Wait for server to be ready
print("⏳ Starting Qwen3-VL server...", flush=True)
for _ in range(60):
    try:
        if requests.get("http://localhost:8080/health").status_code == 200:
            break
    except:
        time.sleep(1)
print("✅ Server ready!\n")

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
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "messages": [
                {
                    "role": "system",
                    "content": "You are a vision AI with access to a live camera. Answer concisely in 1-2 sentences. No lists, no numbering, no speculation.",
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
            "max_tokens": 80,
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "presence_penalty": 1.5,
            "stream": True,
        },
        stream=True,
    )

    print("\n🤖 ", end="", flush=True)
    for line in response.iter_lines():
        if line and line != b"data: [DONE]":
            try:
                chunk = json.loads(line.decode().replace("data: ", ""))
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    print(delta, end="", flush=True)
            except:
                pass
    print("\n")


print("👁️  Commands: 'w' = watch mode, 'q' = quit, or just type a question\n")
try:
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "q":
            break
        elif user_input.lower() == "w":
            print("👁️  Watching... (Ctrl+C to stop)\n")
            try:
                while True:
                    query(
                        "In one sentence, describe what the person is doing right now."
                    )
                    time.sleep(2)
            except KeyboardInterrupt:
                print("\n⏹️  Stopped watching\n")
        elif user_input:
            query(user_input)
finally:
    cap.release()
    server.terminate()
    print("👋 Stopped")
