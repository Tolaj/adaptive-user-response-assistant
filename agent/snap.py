# agent/snap.py
import base64
import subprocess
import tempfile
import os
from PIL import Image
import io

SNAP_WIDTH = 640
SNAP_HEIGHT = 400
JPEG_QUALITY = 60


def snap_screen_b64() -> str:
    """Capture the full macOS screen → base64 JPEG."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            ["screencapture", "-x", tmp_path],
            check=True,
            capture_output=True,
        )
        img = Image.open(tmp_path).convert("RGB")
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
    """Return a PIL Image of the current screen."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            ["screencapture", "-x", tmp_path],
            check=True,
            capture_output=True,
        )
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
        return (2560, 1600)



def snap_screen_with_grid(grid_spacing: int = 25) -> str:
    """
    Take screenshot, RESIZE to 640x400 first, then overlay coordinate grid.
    """
    from PIL import ImageDraw
    import io

    # Get full res screenshot and resize to 640x400 FIRST
    img = snap_screen_pil()
    img = img.resize((SNAP_WIDTH, SNAP_HEIGHT), resample=Image.LANCZOS)

    draw = ImageDraw.Draw(img)

    W = SNAP_WIDTH   # 640
    H = SNAP_HEIGHT  # 400

    # ── Vertical lines + X axis labels ───────────────────────────────────────
    for x in range(0, W + 1, grid_spacing):
        draw.line([(x, 0), (x, H)], fill=(0, 255, 0), width=1)
        if x % 50 == 0:
            draw.text((x + 2, 2),      str(x), fill=(255, 255, 0))
            draw.text((x + 2, H - 12), str(x), fill=(255, 255, 0))

    # ── Horizontal lines + Y axis labels ─────────────────────────────────────
    for y in range(0, H + 1, grid_spacing):
        draw.line([(0, y), (W, y)], fill=(0, 255, 0), width=1)
        if y % 50 == 0:
            draw.text((2,      y + 2), str(y), fill=(255, 255, 0))
            draw.text((W - 25, y + 2), str(y), fill=(255, 255, 0))


    # ── Red dot at every grid intersection ───────────────────────────────────
    # for x in range(0, W + 1, grid_spacing):
    #     for y in range(0, H + 1, grid_spacing):
    #         draw.ellipse([(x-3, y-3), (x+3, y+3)], fill=(255, 0, 0))

    # ── Corner coordinate labels ──────────────────────────────────────────────
    draw.rectangle([(0, 0), (45, 14)],   fill=(0, 0, 0))
    draw.rectangle([(W-50, 0), (W, 14)], fill=(0, 0, 0))
    draw.rectangle([(0, H-14), (45, H)], fill=(0, 0, 0))
    draw.rectangle([(W-55, H-14), (W, H)], fill=(0, 0, 0))
    draw.text((2,      2),      "0,0",     fill=(255, 255, 255))
    draw.text((W - 48, 2),      "640,0",   fill=(255, 255, 255))
    draw.text((2,      H - 12), "0,400",   fill=(255, 255, 255))
    draw.text((W - 53, H - 12), "640,400", fill=(255, 255, 255))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def save_grid_screenshot(path: str = "/tmp/agent_grid_debug.jpg") -> str:
    b64       = snap_screen_with_grid()
    img_bytes = base64.b64decode(b64)
    with open(path, "wb") as f:
        f.write(img_bytes)
    print(f"[Grid] Saved → {path}")
    print(f"[Grid] Open with: open {path}")
    return path


def get_cursor_in_screenshot_space() -> tuple[int, int]:
    """Return current mouse position scaled to 0-640/0-400 space."""
    import pyautogui
    sw, sh = get_screen_size()
    cx, cy = pyautogui.position()
    vx = int(cx * SNAP_WIDTH  / sw)
    vy = int(cy * SNAP_HEIGHT / sh)
    return vx, vy