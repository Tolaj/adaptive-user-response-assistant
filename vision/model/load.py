from config.vlm import VLM_BACKEND
import subprocess
import sys


def load_vlm():
    if VLM_BACKEND == "package":
        return _load_package()
    elif VLM_BACKEND == "server":
        return _load_server()
    else:
        raise ValueError(f"Unknown VLM_BACKEND: {VLM_BACKEND}")


def _load_package():
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Qwen3VLChatHandler
    from config.vlm import VLM_MODEL_PATH, VLM_MMPROJ_PATH

    print("[VLM] Loading Qwen3-VL via package...")
    chat_handler = Qwen3VLChatHandler(clip_model_path=VLM_MMPROJ_PATH)
    llm = Llama(
        model_path=VLM_MODEL_PATH,
        chat_handler=chat_handler,
        n_ctx=2048,
        n_gpu_layers=-1,
        n_batch=512,
        n_threads=8,
        verbose=False,
    )
    print("[VLM] Ready.")
    return llm


def _load_server():
    import subprocess
    import time
    import requests
    from config.vlm import (
        VLM_MODEL_PATH, VLM_MMPROJ_PATH,
        VLM_SERVER_PORT, VLM_SERVER_BINARY
    )

    print("[VLM] Starting llama-server subprocess...")
    proc = subprocess.Popen(
        [
            VLM_SERVER_BINARY,
            "-m", VLM_MODEL_PATH,
            "--mmproj", VLM_MMPROJ_PATH,
            "-ngl", "99",
            "-c", "2048",
            "--port", str(VLM_SERVER_PORT),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://localhost:{VLM_SERVER_PORT}/health"
    print("[VLM] Waiting for server to be ready (may take 2-3 min on first run)...")
    i = 0
    while True:
        # check if process died
        if proc.poll() is not None:
            raise RuntimeError(f"[VLM] Server process died with code {proc.poll()}")
        try:
            if requests.get(url, timeout=1).status_code == 200:
                print(f"[VLM] Server ready after {i}s")
                return proc
        except:
            pass
        if i % 15 == 0 and i > 0:
            print(f"[VLM] Still loading... ({i}s)")
        time.sleep(1)
        i += 1