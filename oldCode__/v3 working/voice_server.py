"""
Voice-Enabled LLM Server
A Flask server that provides voice chat capabilities with local LLMs

Features:
- Speech-to-Text (Whisper)
- Text-to-Speech (gTTS)  
- LLM chat completions
- Complete voice pipeline (talk → AI responds with voice)
"""
# Fix ffmpeg path for Windows

    
import gc
import json
import base64
import tempfile
import time
import threading
from pathlib import Path
from typing import Optional
import io

import torch
import numpy as np
import whisper
from flask import Flask, request, jsonify, Response, stream_with_context, send_file
from flask_cors import CORS
from gtts import gTTS
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Qwen25VLChatHandler
from PIL import Image
import requests

# Import all configuration
from config import *
import subprocess
FFMPEG_PATH = None
# Check common locations
for path in [
    r"C:\ffmpeg\bin\ffmpeg.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"),
]:
    if os.path.exists(path):
        FFMPEG_PATH = path
        break

if FFMPEG_PATH:
    os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ.get("PATH", "")
    print(f"✅ ffmpeg found: {FFMPEG_PATH}")
else:
    print("⚠️ ffmpeg not found in known locations")
# ═══════════════════════════════════════════════════════════════
# FLASK APP SETUP
# ═══════════════════════════════════════════════════════════════

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════
# GLOBAL STATE
# ═══════════════════════════════════════════════════════════════

# Whisper model (Speech-to-Text)
WHISPER_MODEL = None

# LLM model
llm: Optional[Llama] = None
llm_name = ""
llm_path = ""

# Thread lock for LLM access
lock = threading.Lock()


# ═══════════════════════════════════════════════════════════════
# WHISPER (SPEECH-TO-TEXT) LOADING
# ═══════════════════════════════════════════════════════════════

def load_whisper_model():
    """Load Whisper model from local file"""
    global WHISPER_MODEL
    
    if WHISPER_MODEL is not None:
        return  # Already loaded
    
    print(f"🎤 Loading Whisper ({WHISPER_MODEL_NAME})...")
    print(f"   Path: {WHISPER_MODEL_PATH}")
    
    if not WHISPER_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Whisper model not found at: {WHISPER_MODEL_PATH}\n"
            f"Please download and place the model file there."
        )
    
    # Load model directly from checkpoint
    checkpoint = torch.load(str(WHISPER_MODEL_PATH), map_location="cpu")
    dims = whisper.model.ModelDimensions(**checkpoint["dims"])
    model = whisper.model.Whisper(dims)
    model.load_state_dict(checkpoint["model_state_dict"])
    
    WHISPER_MODEL = model
    print(f"✅ Whisper loaded!")


# ═══════════════════════════════════════════════════════════════
# LLM LOADING
# ═══════════════════════════════════════════════════════════════

def find_model_file(model_key: str) -> Path:
    """Find the GGUF model file for a given model key"""
    model_folder = MODELS_DIR / model_key
    gguf_files = [
        f for f in model_folder.glob("*.gguf")
        if not f.name.startswith("mmproj")
    ]
    if not gguf_files:
        raise FileNotFoundError(f"No GGUF model found in {model_folder}")
    return gguf_files[0]


def load_llm_model(model_key: str):
    """Load LLM model into memory"""
    global llm, llm_name, llm_path
    
    # Don't reload if already loaded
    if llm_name == model_key and llm is not None:
        return
    
    print(f"🔄 Loading LLM: {model_key}...")
    
    # Free previous model
    llm = None
    gc.collect()
    time.sleep(1)
    
    # Find model file
    gguf_path = find_model_file(model_key)
    model_folder = MODELS_DIR / model_key
    
    # Check for vision model projection
    mmproj_files = list(model_folder.glob("mmproj*.gguf"))
    mmproj_path = str(mmproj_files[0]) if mmproj_files else None
    
    print(f"   Model: {gguf_path.name}")
    print(f"   GPU Layers: {GPU_LAYERS}")
    print(f"   Context: {CONTEXT_SIZE}")
    
    # Load model
    if mmproj_path:
        # Vision model
        chat_handler = Qwen25VLChatHandler(clip_model_path=mmproj_path)
        llm = Llama(
            model_path=str(gguf_path),
            n_ctx=CONTEXT_SIZE,
            n_threads=CPU_THREADS,
            n_gpu_layers=GPU_LAYERS,
            chat_handler=chat_handler,
            verbose=False,
            flash_attn=LLM_FLASH_ATTN,
            f16_kv=LLM_F16_KV,
            offload_kqv=LLM_OFFLOAD_KQV,
            n_batch=LLM_BATCH_SIZE
        )
    else:
        # Text-only model
        llm = Llama(
            model_path=str(gguf_path),
            n_ctx=CONTEXT_SIZE,
            n_threads=CPU_THREADS,
            n_gpu_layers=GPU_LAYERS,
            verbose=False,
            flash_attn=LLM_FLASH_ATTN,
            n_batch=LLM_BATCH_SIZE
        )
    
    llm_name = model_key
    llm_path = str(gguf_path)
    print(f"✅ LLM loaded: {model_key}")


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def process_image_messages(messages):
    """Process messages that contain images, converting them to base64"""
    for msg in messages:
        if isinstance(msg.get("content"), list):
            for block in msg["content"]:
                if block.get("type") == "image_url":
                    url = block["image_url"]["url"]
                    
                    # Load image
                    if url.startswith("file://"):
                        img_path = Path(url[7:].lstrip("/"))
                        img_data = open(img_path, "rb").read()
                    elif url.startswith("http"):
                        img_data = requests.get(url, timeout=5).content
                    else:
                        continue
                    
                    # Convert to base64
                    img = Image.open(io.BytesIO(img_data))
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    img.thumbnail((448, 448))
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=75, optimize=True)
                    encoded = base64.b64encode(buffered.getvalue()).decode()
                    
                    block["image_url"]["url"] = f"data:image/jpeg;base64,{encoded}"
    
    return messages


def generate_llm_response(messages, max_tokens=512, temperature=0.7, top_p=0.9, stream=False):
    """Generate response from LLM"""
    return llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=stream,
        min_p=0.05,
    )

"""
PASTE THIS FUNCTION into voice_server.py
Replace the repeated soundfile loading code in both voice_chat() and transcribe_audio()
with a call to load_audio_file(tmp_path)
"""

def load_audio_file(path: str) -> np.ndarray:
    """Load any audio file as 16kHz float32 numpy array for Whisper"""
    import soundfile as sf
    audio_data, sample_rate = sf.read(path)
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)
    audio_data = audio_data.astype(np.float32)
    if sample_rate != 16000:
        import resampy
        audio_data = resampy.resample(audio_data, sample_rate, 16000)
    return audio_data

# ═══════════════════════════════════════════════════════════════
# API ROUTES - VOICE
# ═══════════════════════════════════════════════════════════════

@app.route("/v1/audio/transcriptions", methods=["POST"])
def transcribe_audio():
    """
    Speech-to-Text endpoint
    Converts audio file to text using Whisper
    """
    try:
        load_whisper_model()
    except Exception as e:
        return jsonify({"error": f"Whisper not available: {str(e)}"}), 503
    
    if 'file' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['file']
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_file.filename).suffix) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        print("🎤 Transcribing audio...")
        audio_data = load_audio_file(tmp_path)
        result = whisper.transcribe(WHISPER_MODEL, audio_data)

        text = result["text"].strip()
        print(f"📝 Transcription: {text}")
        
        return jsonify({
            "text": text,
            "language": result.get("language", "unknown")
        })
    
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    
    finally:
        try:
            Path(tmp_path).unlink()
        except:
            pass


@app.route("/v1/audio/speech", methods=["POST"])
def text_to_speech():
    """
    Text-to-Speech endpoint
    Converts text to audio using gTTS
    """
    data = request.json
    text = data.get("input", "")
    language = data.get("voice", DEFAULT_TTS_LANGUAGE)
    speed = data.get("speed", DEFAULT_TTS_SPEED)
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        print(f"🔊 Generating speech: {text[:50]}...")
        
        tts = gTTS(text=text, lang=language, slow=(speed < 1.0))
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            tmp_path = tmp.name
        
        response = send_file(
            tmp_path,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="speech.mp3"
        )
        
        # Cleanup after sending
        @response.call_on_close
        def cleanup():
            try:
                Path(tmp_path).unlink()
            except:
                pass
        
        return response
    
    except Exception as e:
        return jsonify({"error": f"TTS failed: {str(e)}"}), 500


@app.route("/v1/voice/chat", methods=["POST"])
def voice_chat():
    """
    Complete voice pipeline endpoint
    audio → transcribe → LLM → text-to-speech → audio
    """
    # Load models
    try:
        load_whisper_model()
    except Exception as e:
        return jsonify({"error": f"Whisper not available: {str(e)}"}), 503
    
    if llm is None:
        return jsonify({"error": "LLM not loaded"}), 503
    
    if 'file' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['file']
    language = request.form.get('voice', DEFAULT_TTS_LANGUAGE)
    
    # STEP 1: Transcribe audio to text
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio_file.save(tmp.name)
        tmp.flush()
        tmp_path = tmp.name
    
    try:
        print("🎤 Step 1/3: Transcribing...")
        audio_data = load_audio_file(tmp_path)
        result = whisper.transcribe(WHISPER_MODEL, audio_data)
        user_text = result["text"].strip()
        print(f"   User: {user_text}")
    except Exception as e:
        import traceback
        print(f"❌ Transcription error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    finally:
        try:
            Path(tmp_path).unlink()
        except:
            pass
    
    # STEP 2: Get LLM response
    print("🤖 Step 2/3: Getting LLM response...")
    messages = [
        {"role": "system", "content": VOICE_ASSISTANT_PROMPT},
        {"role": "user", "content": user_text}
    ]
    
    try:
        with lock:
            output = generate_llm_response(
                messages,
                max_tokens=VOICE_MAX_TOKENS,
                temperature=VOICE_TEMPERATURE
            )
        
        assistant_text = output["choices"][0]["message"]["content"]
        print(f"   Assistant: {assistant_text}")
    except Exception as e:
        return jsonify({"error": f"LLM failed: {str(e)}"}), 500
    
    # STEP 3: Convert response to speech
    print("🔊 Step 3/3: Generating speech...")
    try:
        tts = gTTS(text=assistant_text, lang=language, slow=False)
        
        # Save to accessible temp directory
        temp_dir = Path(tempfile.gettempdir()) / "voice_chat"
        temp_dir.mkdir(exist_ok=True)
        
        audio_filename = f"response_{int(time.time())}.mp3"
        audio_path = temp_dir / audio_filename
        tts.save(str(audio_path))
        
        print("✅ Voice chat complete!")
        
        return jsonify({
            "user_text": user_text,
            "response_text": assistant_text,
            "audio_path": str(audio_path),
            "audio_url": f"/temp/audio/{audio_filename}"
        })
    
    except Exception as e:
        return jsonify({"error": f"TTS failed: {str(e)}"}), 500


@app.route("/temp/audio/<filename>", methods=["GET"])
def serve_audio(filename):
    """Serve temporary audio files"""
    temp_dir = Path(tempfile.gettempdir()) / "voice_chat"
    file_path = temp_dir / filename
    
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    
    return send_file(file_path, mimetype="audio/mpeg")


# ═══════════════════════════════════════════════════════════════
# API ROUTES - LLM
# ═══════════════════════════════════════════════════════════════

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """Standard chat completions endpoint (OpenAI compatible)"""
    if llm is None:
        return jsonify({"error": "LLM not loaded"}), 503
    
    data = request.json
    messages = data.get("messages")
    max_tokens = data.get("max_tokens", 512)
    temperature = data.get("temperature", 0.7)
    top_p = data.get("top_p", 0.9)
    stream = data.get("stream", False)
    
    if not messages:
        return jsonify({"error": "messages required"}), 400
    
    messages = process_image_messages(messages)
    
    if stream:
        return stream_response(messages, max_tokens, temperature, top_p)
    
    # Non-streaming response
    start = time.time()
    
    with lock:
        output = generate_llm_response(messages, max_tokens, temperature, top_p)
    
    text = output["choices"][0]["message"]["content"]
    elapsed = time.time() - start
    
    return jsonify({
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "model": llm_name,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": text},
            "finish_reason": "stop",
        }],
        "usage": {"completion_time": round(elapsed, 2)},
    })


def stream_response(messages, max_tokens, temperature, top_p):
    """Stream LLM response"""
    def generate():
        with lock:
            stream = generate_llm_response(messages, max_tokens, temperature, top_p, stream=True)
            
            for chunk in stream:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    data = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "model": llm_name,
                        "choices": [{
                            "delta": {"content": delta["content"]},
                            "index": 0,
                            "finish_reason": None,
                        }],
                    }
                    yield f"data: {json.dumps(data)}\n\n"
        
        yield "data: [DONE]\n\n"
    
    return Response(stream_with_context(generate()), mimetype="text/event-stream")


# ═══════════════════════════════════════════════════════════════
# API ROUTES - UTILITY
# ═══════════════════════════════════════════════════════════════

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "llm_model": llm_name,
        "llm_loaded": llm is not None,
        "whisper_model": WHISPER_MODEL_NAME,
        "whisper_loaded": WHISPER_MODEL is not None,
        "gpu_layers": GPU_LAYERS,
        "context_size": CONTEXT_SIZE,
    })


@app.route("/v1/models", methods=["GET"])
def list_models():
    """List available models"""
    data = []
    for key in AVAILABLE_LLM_MODELS:
        try:
            path = find_model_file(key)
            exists = True
        except:
            path = None
            exists = False
        
        data.append({
            "id": key,
            "object": "model",
            "owned_by": "local",
            "available": exists,
            "path": str(path) if path else None,
        })
    
    return jsonify({"object": "list", "data": data})


@app.route("/models/switch", methods=["POST"])
def switch_model():
    """Switch to a different LLM model"""
    data = request.json
    model_key = data.get("model")
    
    if model_key not in AVAILABLE_LLM_MODELS:
        return jsonify({"error": "Invalid model"}), 400
    
    try:
        load_llm_model(model_key)
        return jsonify({"status": "ok", "model": model_key})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎙️  VOICE-ENABLED LLM SERVER")
    print("="*60)
    
    # Show configuration
    print_config()
    
    # Load LLM on startup
    try:
        load_llm_model(ACTIVE_LLM_MODEL)
    except Exception as e:
        print(f"❌ Failed to load LLM: {e}")
        print("Server will start but LLM features won't work")
    
    # Start server
    print(f"\n✨ Server starting on http://localhost:{SERVER_PORT}")
    print("\n📡 Available endpoints:")
    print("   POST /v1/audio/transcriptions  - Speech to text")
    print("   POST /v1/audio/speech          - Text to speech")
    print("   POST /v1/voice/chat            - Complete voice pipeline")
    print("   POST /v1/chat/completions      - LLM chat")
    print("   GET  /health                   - Server status")
    print("   GET  /v1/models                - List models")
    print()
    
    app.run(host="0.0.0.0", port=SERVER_PORT, threaded=True)
