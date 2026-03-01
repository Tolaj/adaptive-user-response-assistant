"""
llm/llm_engine.py

Loads a GGUF model via llama-cpp-python and exposes a streaming generator.
Singleton — model is loaded once on first call.

Usage:
    from llm.llm_engine import stream_response

    for token in stream_response("Hello, who are you?"):
        print(token, end="", flush=True)
"""

import threading
import glob
from pathlib import Path
from typing import Generator, Optional

from llama_cpp import Llama

from config import (
    MODELS_DIR,
    ACTIVE_LLM_MODEL,
    GPU_LAYERS,
    CONTEXT_SIZE,
    CPU_THREADS,
    VOICE_SYSTEM_PROMPT,
    VOICE_MAX_TOKENS,
    VOICE_TEMPERATURE,
)

# ── Model path resolution ──────────────────────────────────────────────────────


def _find_model_path() -> str:
    """
    Find the GGUF file inside models/<ACTIVE_LLM_MODEL>/.
    Prefers quantized variants in this order: Q4_K_M, Q4, Q5, Q8, fallback first found.
    """
    model_dir = MODELS_DIR / ACTIVE_LLM_MODEL
    if not model_dir.exists():
        raise FileNotFoundError(f"Model directory not found: {model_dir}")

    gguf_files = sorted(model_dir.glob("*.gguf"))
    if not gguf_files:
        raise FileNotFoundError(f"No .gguf files found in {model_dir}")

    # Prefer common good-quality quants
    preference = ["Q4_K_M", "Q4_K_S", "Q4", "Q5_K_M", "Q5", "Q8", "q4", "q5", "q8"]
    for pref in preference:
        for f in gguf_files:
            if pref.lower() in f.name.lower():
                return str(f)

    return str(gguf_files[0])  # fallback: first found


# ── Singleton ─────────────────────────────────────────────────────────────────

_model: Optional[Llama] = None
_lock = threading.Lock()
_model_path: Optional[str] = None


def get_llm() -> Llama:
    global _model, _model_path
    if _model is not None:
        return _model

    with _lock:
        if _model is not None:
            return _model

        path = _find_model_path()
        _model_path = path
        print(f"[LLM] Loading model from: {path}")
        print(
            f"[LLM] GPU layers: {GPU_LAYERS} | Context: {CONTEXT_SIZE} | Threads: {CPU_THREADS}"
        )

        _model = Llama(
            model_path=path,
            n_gpu_layers=GPU_LAYERS,
            n_ctx=CONTEXT_SIZE,
            n_threads=CPU_THREADS,
            verbose=False,
        )
        print("[LLM] Model ready.")

    return _model


def is_loaded() -> bool:
    return _model is not None


def get_model_path() -> Optional[str]:
    return _model_path


# ── Conversation history ───────────────────────────────────────────────────────


class ConversationHistory:
    """Simple rolling conversation history with token budget."""

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self._history: list[dict] = []

    def add_user(self, text: str):
        self._history.append({"role": "user", "content": text})
        self._trim()

    def add_assistant(self, text: str):
        self._history.append({"role": "assistant", "content": text})
        self._trim()

    def get_messages(self) -> list[dict]:
        return [{"role": "system", "content": VOICE_SYSTEM_PROMPT}] + self._history

    def clear(self):
        self._history = []

    def _trim(self):
        # Keep last max_turns * 2 messages (user+assistant pairs)
        if len(self._history) > self.max_turns * 2:
            self._history = self._history[-(self.max_turns * 2) :]


# ── Streaming inference ────────────────────────────────────────────────────────


def stream_response(
    user_text: str,
    history: Optional[ConversationHistory] = None,
) -> Generator[str, None, str]:
    """
    Yields tokens one by one as the LLM generates them.
    Adds the exchange to history if provided.
    Returns the full response text when exhausted.

    Usage:
        full = ""
        for token in stream_response("Hi!", history):
            print(token, end="", flush=True)
            full += token
    """
    llm = get_llm()

    if history:
        history.add_user(user_text)
        messages = history.get_messages()
    else:
        messages = [
            {"role": "system", "content": VOICE_SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ]

    full_response = ""

    try:
        stream = llm.create_chat_completion(
            messages=messages,
            max_tokens=VOICE_MAX_TOKENS,
            temperature=VOICE_TEMPERATURE,
            stream=True,
        )

        for chunk in stream:
            delta = chunk["choices"][0]["delta"]
            token = delta.get("content", "")
            if token:
                full_response += token
                yield token

    except Exception as e:
        error_msg = f"[LLM error: {e}]"
        yield error_msg
        full_response = error_msg

    if history and full_response:
        history.add_assistant(full_response)

    return full_response
