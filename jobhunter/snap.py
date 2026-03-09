# jobhunter/snap.py
# ─────────────────────────────────────────────────────────────────────────────
# Captures the current browser page as a base64 JPEG.
# Mirrors vision/inference/snap.py — same interface, different source.
# Instead of webcam → we capture the Playwright browser page.
# ─────────────────────────────────────────────────────────────────────────────

import base64
from jobhunter.config import JPEG_QUALITY


def snap_browser_b64() -> str:
    """
    Screenshot the current browser page → base64 JPEG string.
    Drop-in replacement for vision/inference/snap.py snap_b64().
    """
    from jobhunter.browser import get_browser

    page = get_browser()

    # Full PNG screenshot from Playwright
    png_bytes = page.screenshot(full_page=False)  # viewport only — faster

    # Convert PNG → JPEG for smaller payload (same as camera pipeline)
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    return base64.b64encode(buf.getvalue()).decode()