# agent/tools/omniparser.py

from __future__ import annotations

import threading
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from config.agent import OMNIPARSER_WEIGHTS_DIR, OMNIPARSER_CAPTION_MODEL

_yolo_model = None
_caption_model = None
_processor = None
_device = None
_lock = threading.Lock()


def _resolve_device() -> str:
    import torch

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _cache_is_valid(past_key_values) -> bool:
    if past_key_values is None:
        return False
    if not isinstance(past_key_values, (list, tuple)) or len(past_key_values) == 0:
        return False
    if past_key_values[0] is None:
        return False
    if (
        not isinstance(past_key_values[0], (list, tuple))
        or len(past_key_values[0]) == 0
    ):
        return False
    if past_key_values[0][0] is None:
        return False
    return True


def _patch_language_model(florence_model):
    import inspect

    for name, module in florence_model.named_modules():
        method = getattr(type(module), "prepare_inputs_for_generation", None)
        if method is None:
            continue
        try:
            src = inspect.getsource(method)
        except Exception:
            continue
        if "past_key_values[0][0].shape" not in src:
            continue

        orig = method

        def _make_patched(original):
            def _patched(self, input_ids, past_key_values=None, **kwargs):
                if not _cache_is_valid(past_key_values):
                    return {
                        "input_ids": input_ids,
                        "past_key_values": None,
                        "use_cache": kwargs.get("use_cache", True),
                        "attention_mask": kwargs.get("attention_mask"),
                    }
                return original(
                    self, input_ids, past_key_values=past_key_values, **kwargs
                )

            return _patched

        setattr(type(module), "prepare_inputs_for_generation", _make_patched(orig))
        print(
            f"[OmniParser] Patched prepare_inputs_for_generation on {name or 'root'} ({type(module).__name__})"
        )


def _get_parser():
    global _yolo_model, _caption_model, _processor, _device

    if _yolo_model is not None:
        return _yolo_model, _caption_model, _processor, _device

    with _lock:
        if _yolo_model is not None:
            return _yolo_model, _caption_model, _processor, _device

        import torch

        _device = _resolve_device()
        print(f"[OmniParser] Using device: {_device}")

        weights = Path(OMNIPARSER_WEIGHTS_DIR)
        icon_model_path = str(weights / "icon_detect" / "model.pt")

        print(f"[OmniParser] Loading YOLO detector from {icon_model_path} ...")
        from ultralytics import YOLO

        _yolo_model = YOLO(icon_model_path)
        _yolo_model.overrides["verbose"] = False

        if OMNIPARSER_CAPTION_MODEL == "florence2":
            from transformers import AutoProcessor, AutoModelForCausalLM

            caption_path = str(weights / "icon_caption_florence")
            print(f"[OmniParser] Loading Florence-2 from {caption_path} ...")

            _processor = AutoProcessor.from_pretrained(
                caption_path, trust_remote_code=True
            )
            _caption_model = (
                AutoModelForCausalLM.from_pretrained(
                    caption_path,
                    dtype=torch.float32,
                    trust_remote_code=True,
                    attn_implementation="eager",
                )
                .to(_device)
                .eval()
            )

            _patch_language_model(_caption_model)

        else:
            from transformers import Blip2Processor, Blip2ForConditionalGeneration

            caption_path = str(weights / "icon_caption_blip2")
            print(f"[OmniParser] Loading BLIP2 from {caption_path} ...")
            _processor = Blip2Processor.from_pretrained(caption_path)
            _caption_model = Blip2ForConditionalGeneration.from_pretrained(
                caption_path,
                torch_dtype=torch.float32,
                device_map="auto",
            ).eval()

        print("[OmniParser] Ready.")

    return _yolo_model, _caption_model, _processor, _device


# ── Batched captioning ──────────────────────────────────────────────────────
BATCH_SIZE = 8  # process 8 crops at once — tune up if VRAM allows


def _caption_crops_batch(crops: list[Image.Image]) -> list[str]:
    """Caption a list of crops in batches. Much faster than one-by-one."""
    import torch

    _, caption_model, processor, device = _get_parser()
    labels = []

    for i in range(0, len(crops), BATCH_SIZE):
        batch = crops[i : i + BATCH_SIZE]
        try:
            if OMNIPARSER_CAPTION_MODEL == "florence2":
                inputs = processor(
                    images=batch,
                    text=["<CAPTION>"] * len(batch),
                    return_tensors="pt",
                    padding=True,
                ).to(device)
                with torch.no_grad():
                    ids = caption_model.generate(
                        input_ids=inputs["input_ids"],
                        pixel_values=inputs["pixel_values"],
                        max_new_tokens=20,
                    )
                raws = processor.batch_decode(ids, skip_special_tokens=True)
                for r in raws:
                    labels.append(r.replace("<CAPTION>", "").strip())
            else:
                inputs = processor(images=batch, return_tensors="pt", padding=True).to(
                    device
                )
                with torch.no_grad():
                    ids = caption_model.generate(**inputs, max_new_tokens=20)
                for j in range(len(batch)):
                    labels.append(
                        processor.decode(ids[j], skip_special_tokens=True).strip()
                    )
        except Exception as e:
            print(f"[OmniParser] Batch caption failed: {e}")
            labels.extend(["unknown"] * len(batch))

    return labels


def parse(
    img: Image.Image,
    conf_threshold: float = 0.05,
    draw_labels: bool = True,
) -> tuple[Image.Image, list[dict]]:
    yolo, _, _, _ = _get_parser()

    orig_w, orig_h = img.size
    detect_img = img.resize((640, 640), Image.LANCZOS)
    sx = orig_w / 640
    sy = orig_h / 640

    results = yolo(detect_img, conf=conf_threshold, verbose=False)[0]
    boxes = results.boxes

    annotated = img.copy()
    draw = ImageDraw.Draw(annotated)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except Exception:
        font = ImageFont.load_default()

    # ── Collect all valid crops first ──────────────────────────────────────
    box_meta = []
    crops = []

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])

        x1o = int(x1 * sx)
        y1o = int(y1 * sy)
        x2o = int(x2 * sx)
        y2o = int(y2 * sy)
        cx = (x1o + x2o) // 2
        cy = (y1o + y2o) // 2
        w = x2o - x1o
        h = y2o - y1o

        margin = 4
        left = max(0, x1o - margin)
        top = max(0, y1o - margin)
        right = min(orig_w, x2o + margin)
        bottom = min(orig_h, y2o + margin)

        box_meta.append(
            (
                i + 1,
                cx,
                cy,
                w,
                h,
                round(conf, 3),
                x1o,
                y1o,
                x2o,
                y2o,
                left,
                top,
                right,
                bottom,
            )
        )

        if right - left < 4 or bottom - top < 4:
            crops.append(None)  # placeholder — will become "unknown"
        else:
            crop = img.crop((left, top, right, bottom)).convert("RGB")
            if crop.width < 16 or crop.height < 16:
                crop = crop.resize(
                    (max(crop.width, 16), max(crop.height, 16)), Image.LANCZOS
                )
            crops.append(crop)

    # ── Batch caption all valid crops in one go ────────────────────────────
    valid_crops = [c for c in crops if c is not None]
    valid_indices = [i for i, c in enumerate(crops) if c is not None]

    labels_valid = _caption_crops_batch(valid_crops) if valid_crops else []

    # Map back to original indices
    label_map = {}
    for idx, label in zip(valid_indices, labels_valid):
        label_map[idx] = label

    # ── Build element list + annotate ──────────────────────────────────────
    elements = []
    for i, meta in enumerate(box_meta):
        elem_id, cx, cy, w, h, conf, x1o, y1o, x2o, y2o, *_ = meta
        label = label_map.get(i, "unknown")

        elements.append(
            {
                "id": elem_id,
                "label": label,
                "x": cx,
                "y": cy,
                "w": w,
                "h": h,
                "conf": conf,
            }
        )

        if draw_labels:
            color = _id_color(elem_id)
            draw.rectangle([x1o, y1o, x2o, y2o], outline=color, width=2)
            tag = str(elem_id)
            bbox = draw.textbbox((0, 0), tag, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.rectangle([x1o, y1o - th - 4, x1o + tw + 6, y1o], fill=color)
            draw.text((x1o + 3, y1o - th - 3), tag, fill="white", font=font)

    print(f"[OmniParser] {len(elements)} elements detected and captioned.")
    return annotated, elements


def elements_to_text(elements: list[dict]) -> str:
    if not elements:
        return "No interactive elements detected."
    lines = ["Detected UI elements (id | label | center x,y):"]
    for el in elements:
        lines.append(
            f"  [{el['id']:2d}]  {el['label'][:40]:40s}  "
            f"x={el['x']:4d}  y={el['y']:4d}"
        )
    return "\n".join(lines)


def _id_color(elem_id: int) -> str:
    palette = [
        "#E94B3B",
        "#2BC0E4",
        "#F5A623",
        "#7ED321",
        "#BD10E0",
        "#4A90E2",
        "#D0021B",
        "#417505",
        "#9013FE",
        "#F8E71C",
    ]
    return palette[(elem_id - 1) % len(palette)]
