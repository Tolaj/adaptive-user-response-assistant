import numpy as np


def encode_text(
    texts: list[str],
    model: dict,
    voice: str,
    speed: float,
    language: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Tokenise + encode texts. Returns (hidden, durations, attn_mask, style)."""
    from tts.model.voices import load_style

    tagged = [f"<{language}>{t}</{language}>" for t in texts]
    inputs = model["tokenizer"](
        tagged, return_tensors="np", padding=True, truncation=True
    )
    ids, attn = inputs["input_ids"], inputs["attention_mask"]
    style = load_style(voice, model["model_path"]).repeat(ids.shape[0], axis=0)
    hidden, raw_dur = model["text_encoder"].run(
        None, {"input_ids": ids, "attention_mask": attn, "style": style}
    )
    durations = (raw_dur / speed * model["sample_rate"]).astype(np.int64)
    return hidden, durations, attn, style
