import subprocess
import sys
from pathlib import Path
from config.vlm import VLM_BACKEND


def _ensure_downloaded() -> None:
    from config.vlm import VLM_MODEL_PATH, VLM_MMPROJ_PATH
    import warnings

    model_path = Path(VLM_MODEL_PATH)
    mmproj_path = Path(VLM_MMPROJ_PATH)

    if model_path.exists() and mmproj_path.exists():
        return

    print("[VLM] Model files not found — downloading from HuggingFace...")
    model_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        raise RuntimeError("huggingface_hub not installed. Run: pip install huggingface_hub")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if not model_path.exists():
            print(f"[VLM] Downloading {model_path.name} (~1.5 GB)...")
            hf_hub_download(
                repo_id="Qwen/Qwen3-VL-2B-Instruct-GGUF",
                filename="Qwen3VL-2B-Instruct-Q4_K_M.gguf",
                local_dir=str(model_path.parent),
            )
            print(f"[VLM] Downloaded {model_path.name}")

        if not mmproj_path.exists():
            print(f"[VLM] Downloading {mmproj_path.name} (~445 MB)...")
            hf_hub_download(
                repo_id="ggml-org/Qwen3-VL-2B-Instruct-GGUF",
                filename="mmproj-Qwen3-VL-2B-Instruct-Q8_0.gguf",
                local_dir=str(mmproj_path.parent),
            )
            print(f"[VLM] Downloaded {mmproj_path.name}")

    print("[VLM] All model files ready.")


    
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

    _ensure_downloaded()
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
    import time
    import requests
    from config.vlm import (
        VLM_MODEL_PATH, VLM_MMPROJ_PATH,
        VLM_SERVER_PORT, VLM_SERVER_BINARY
    )

    _ensure_downloaded()

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