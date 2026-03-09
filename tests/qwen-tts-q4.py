import os
import re
import time
import warnings
import threading
import numpy as np
import sounddevice as sd
import mlx.core as mx
from queue import Queue, Empty
from pathlib import Path
from mlx_audio.tts.utils import load_model

warnings.filterwarnings("ignore", message=".*incorrect regex pattern.*", category=UserWarning)

# --- CONFIG ---
mx.set_cache_limit(2 * 1024 * 1024 * 1024)

cache_dir = Path(__file__).parent / "models" / "qwen-tts"
os.environ["HF_HOME"] = str(cache_dir)
os.environ["HUGGINGFACE_HUB_CACHE"] = str(cache_dir)

SAMPLE_RATE = 24000
VOICE       = "Chelsie"
MAX_WORDS   = 8

PREGENERATIONS = {
    "thinking" : "One moment...",
    "greeting" : "Hey, how can I help?",
    "confirm"  : "Got it.",
    "error"    : "Sorry, I didn't catch that.",
    "sure"     : "Sure.",
    "welcome"  : "You're welcome.",
}

audio_cache = {}

# --- MODEL LOAD ---
print("Loading model...")
model = load_model("mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit")
print("Model loaded.\n")

# Single serial queue — all generate() calls go through here in order.
# This eliminates races without holding a lock across a long generation.
_gen_queue  = Queue()
_gen_result = Queue()

def _generation_worker():
    """Single worker thread that owns all model.generate() calls."""
    while True:
        task = _gen_queue.get()
        if task is None:
            break
        text, stream_cb, result_q = task
        chunks = []
        first = True
        t0 = time.time()
        try:
            for result in model.generate(text=text, voice=VOICE):
                chunk = np.array(result.audio, dtype=np.float32)
                max_val = np.max(np.abs(chunk))
                if max_val > 0:
                    chunk /= max_val
                if first:
                    print(f"  first audio: {time.time() - t0:.2f}s")
                    first = False
                if stream_cb:
                    stream_cb(chunk)
                chunks.append(chunk)
        except Exception as e:
            print(f"  generation error: {e}")
        finally:
            # Clear MLX cache after each generation to prevent memory buildup
            mx.metal.clear_cache()

        if result_q is not None:
            audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.float32)
            result_q.put(audio)

_worker_thread = threading.Thread(target=_generation_worker, daemon=True)
_worker_thread.start()


def _generate_blocking(text):
    """Submit to worker and block until full audio is returned."""
    result_q = Queue()
    _gen_queue.put((text, None, result_q))
    return result_q.get()


def _split_sentences(text):
    parts = re.split(r'(?<=[.!?,])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]


def _truncate(text, max_words=MAX_WORDS):
    words = text.split()
    return text if len(words) <= max_words else ' '.join(words[:max_words])


def _play(audio):
    if len(audio) == 0:
        return
    sd.play(audio, samplerate=SAMPLE_RATE)
    sd.wait()


# --- PRE-BAKE CACHE ---

def _prebake_all():
    for key, phrase in PREGENERATIONS.items():
        try:
            audio_cache[key] = _generate_blocking(phrase)
            print(f"  cached: '{key}'")
        except Exception as e:
            print(f"  cache failed for '{key}': {e}")
    print("  All phrases cached. GPU is warm.\n")

threading.Thread(target=_prebake_all, daemon=True).start()


def play_cached(key):
    if key in audio_cache:
        _play(audio_cache[key])
    else:
        print(f"  ('{key}' not cached yet, generating live)")
        _play(_generate_blocking(PREGENERATIONS.get(key, key)))


# --- STREAMING PLAYBACK ---

def speak_streaming(text):
    """Submit to worker with a stream callback — plays chunks as they arrive."""
    stream = sd.OutputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    stream.start()
    done = threading.Event()

    def on_chunk(chunk):
        stream.write(chunk)

    result_q = Queue()
    _gen_queue.put((text, on_chunk, result_q))
    result_q.get()  # block until generation done

    stream.stop()
    stream.close()


# --- PIPELINED PLAYBACK ---

def speak_pipelined(sentences):
    """Queue all sentences; play each as soon as it's ready."""
    result_qs = []
    for s in sentences:
        rq = Queue()
        _gen_queue.put((s, None, rq))
        result_qs.append(rq)

    first = True
    t0 = time.time()
    for rq in result_qs:
        audio = rq.get()
        if first:
            print(f"  first audio (pipeline): {time.time() - t0:.2f}s")
            first = False
        _play(audio)


# --- MAIN SPEAK ---

def speak(text):
    text = text.strip()
    if not text:
        return

    if len(text.split()) <= MAX_WORDS:
        speak_streaming(text)
        return

    sentences = _split_sentences(text)
    if len(sentences) == 1:
        short = _truncate(text, MAX_WORDS)
        rest  = ' '.join(text.split()[MAX_WORDS:])
        sentences = [short, rest] if rest else [short]

    speak_pipelined(sentences)


# --- REPL ---

print("-" * 45)
print("Tips:")
print("  <=8 words            -> streamed (fastest)")
print("  Longer text          -> auto-pipelined")
print("  :thinking / :confirm -> instant cached audio")
print("-" * 45, "\n")

while True:
    try:
        text = input("Enter text: ").strip()
        if not text:
            continue

        if text.startswith(":"):
            key = text[1:]
            if key in PREGENERATIONS:
                play_cached(key)
            else:
                print(f"  Unknown key. Available: {list(PREGENERATIONS.keys())}")
            continue

        speak(text)

    except KeyboardInterrupt:
        _gen_queue.put(None)  # clean shutdown
        print("\nBye.")
        break