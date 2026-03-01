"""
llm/llm.py
LLM inference — plug your model in here.

Expected interface (keep this signature so server.py works as-is):

    generate_response(text: str) -> str

Steps to implement:
  1. Load your model (llama-cpp, transformers, ollama, etc.)
  2. Fill in generate_response() below
  3. Uncomment the two LLM lines in server.py
"""

from config import (
    ACTIVE_LLM_MODEL,
    GPU_LAYERS,
    CONTEXT_SIZE,
    CPU_THREADS,
    VOICE_SYSTEM_PROMPT,
    VOICE_MAX_TOKENS,
    VOICE_TEMPERATURE,
)

# TODO: load your model here
# model = ...


def generate_response(text: str) -> str:
    """Take transcribed user text, return LLM reply string."""
    raise NotImplementedError("LLM not wired up yet")