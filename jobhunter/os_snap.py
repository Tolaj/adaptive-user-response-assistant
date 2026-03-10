# jobhunter/os_snap.py
# ─────────────────────────────────────────────────────────────────────────────
# macOS screen capture → base64 JPEG
# Uses native screencapture — no Playwright, no OpenCV dependency for screen.
# Drop-in replacement for jobhunter/snap.py but captures the REAL screen.
# ─────────────────────────────────────────────────────────────────────────────

import base64
import subprocess
import tempfile
import os
from PIL import Image
import io

# Resolution to send to VLM — big enough to read text, small enough to be fast
SNAP_WIDTH  = 640
SNAP_HEIGHT = 400
JPEG_QUALITY = 60


def snap_screen_b64() -> str:
    """
    Capture the full macOS screen → base64 JPEG string.
    Uses `screencapture -x` (silent, no shutter sound).
    """
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # -x = no sound, -1 = main display only
        subprocess.run(
            ["screencapture", "-x", tmp_path],
            check=True,
            capture_output=True,
        )
        img = Image.open(tmp_path).convert("RGB")
        img = img.transpose(Image.FLIP_LEFT_RIGHT)  # ← add this
        # Resize to VLM-friendly resolution (keeps aspect ratio, pads if needed)
        img.thumbnail((SNAP_WIDTH, SNAP_HEIGHT), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=JPEG_QUALITY)
        return base64.b64encode(buf.getvalue()).decode()

    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def snap_screen_pil() -> Image.Image:
    """Return a PIL Image of the current screen (useful for coordinate mapping)."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(["screencapture", "-x", "-1", tmp_path], check=True, capture_output=True)
        return Image.open(tmp_path).convert("RGB")
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def get_screen_size() -> tuple[int, int]:
    """Return actual screen resolution (width, height)."""
    try:
        import pyautogui
        return pyautogui.size()
    except Exception:
        return (2560, 1600)  # safe fallback for Retina MacBook


if __name__ == "__main__":
    b64 = snap_screen_b64()
    print(f"[os_snap] Screenshot captured: {len(b64)} base64 chars")