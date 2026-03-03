import os
import sys
from pathlib import Path
from contextlib import contextmanager
from llama_cpp import Llama
from config.llm import GPU_LAYERS, CONTEXT_SIZE, CPU_THREADS


@contextmanager
def _suppress_native_startup_output(enabled: bool = True):
    """Temporarily redirect process stdout/stderr to /dev/null.

    This suppresses verbose native llama.cpp / ggml startup logs on macOS.
    """
    if not enabled:
        yield
        return

    sys.stdout.flush()
    sys.stderr.flush()

    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    saved_stdout_fd = os.dup(1)
    saved_stderr_fd = os.dup(2)
    try:
        os.dup2(devnull_fd, 1)
        os.dup2(devnull_fd, 2)
        yield
    finally:
        os.dup2(saved_stdout_fd, 1)
        os.dup2(saved_stderr_fd, 2)
        os.close(saved_stdout_fd)
        os.close(saved_stderr_fd)
        os.close(devnull_fd)


def load_llm(
    path: str | Path,
    gpu_layers: int = GPU_LAYERS,
    ctx: int = CONTEXT_SIZE,
    threads: int = CPU_THREADS,
) -> Llama:

    print(f"[LLM] Loading: {path} \n")
    print(f"[LLM] GPU={gpu_layers}  ctx={ctx}  threads={threads}")
    with _suppress_native_startup_output(enabled=True):
        model = Llama(
            model_path=str(path),
            n_gpu_layers=gpu_layers,
            n_ctx=ctx,
            n_threads=threads,
            verbose=False,
        )
    print("[LLM] Ready.")
    return model
