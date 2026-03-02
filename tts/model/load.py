import os
import onnxruntime as ort
from transformers import PreTrainedTokenizerFast


def load_supertonic(model_path: str) -> dict:
    """Load Supertonic 2 ONNX sessions dict."""
    opts = ort.SessionOptions()
    opts.log_severity_level = 3
    onnx_dir = os.path.join(model_path, "onnx")
    tokenizer_file = os.path.join(model_path, "tokenizer.json")
    print(f"[Supertonic] Loading from {model_path} ...\n")
    sessions = {
        "tokenizer": PreTrainedTokenizerFast(
            tokenizer_file=tokenizer_file,
            model_max_length=1000,
            pad_token=" ",
        ),
        "text_encoder": ort.InferenceSession(
            os.path.join(onnx_dir, "text_encoder.onnx"), opts
        ),
        "latent_denoiser": ort.InferenceSession(
            os.path.join(onnx_dir, "latent_denoiser.onnx"), opts
        ),
        "voice_decoder": ort.InferenceSession(
            os.path.join(onnx_dir, "voice_decoder.onnx"), opts
        ),
        "model_path": model_path,
        "sample_rate": 44100,
        "chunk_compress_factor": 6,
        "base_chunk_size": 512,
        "latent_dim": 24,
        "style_dim": 128,
        "latent_size": 512 * 6,  # 3072
    }
    print("[Supertonic] Ready.")
    return sessions
