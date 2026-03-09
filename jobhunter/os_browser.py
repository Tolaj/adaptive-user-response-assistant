# jobhunter/os_browser.py
# ─────────────────────────────────────────────────────────────────────────────
# Real OS-level Chrome automation via pyautogui.
# No Playwright. Moves the ACTUAL mouse, types on the ACTUAL keyboard.
#
# Flow:
#   1. launch_chrome()          → open Chrome via macOS `open` command
#   2. select_profile(email)    → VLM sees profile picker, clicks right one
#   3. navigate(url)            → Cmd+L → type URL → Enter
#   4. click(x, y)              → raw mouse click (VLM-guided coordinates)
#   5. type_text(text)          → keyboard typing with human-like delay
#
# Coordinate system: VLM returns coords in SNAP_WIDTH×SNAP_HEIGHT space.
# We scale them to actual screen resolution before clicking.
# ─────────────────────────────────────────────────────────────────────────────

import time
import subprocess
import pyautogui
from jobhunter.os_snap import snap_screen_b64, get_screen_size, SNAP_WIDTH, SNAP_HEIGHT
from jobhunter.logger import log

# Safety: pyautogui raises exception if mouse hits screen corner
pyautogui.FAILSAFE = True
# Small pause between pyautogui actions to feel human
pyautogui.PAUSE = 0.05


# ── Coordinate scaling ─────────────────────────────────────────────────────
def _scale_coords(vx: int, vy: int) -> tuple[int, int]:
    sw, sh = get_screen_size()
    vx = max(0, min(vx, 640))
    vy = max(0, min(vy, 400))
    x = int(vx * sw / 640)
    y = int(vy * sh / 400)
    return x, y

def find_text_on_screen(text: str) -> tuple[int, int] | None:
    """Find exact screen coordinates of any visible text using OCR."""
    import pytesseract
    from PIL import Image
    import subprocess, tempfile, os

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(["screencapture", "-x", tmp_path], check=True, capture_output=True)
        img = Image.open(tmp_path)
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        text_lower = text.lower()
        for i, word in enumerate(data["text"]):
            if text_lower in word.lower() and int(data["conf"][i]) > 30:
                x = data["left"][i] + data["width"][i] // 2
                y = data["top"][i] + data["height"][i] // 2
                # Convert from physical to logical pixels on Retina
                sw, sh = get_screen_size()
                img_w, img_h = img.size
                lx = int(x * sw / img_w)
                ly = int(y * sh / img_h)
                log(f"[OCR] Found '{word}' at logical ({lx},{ly})")
                return lx, ly
    except Exception as e:
        log(f"[OCR] {e}")
    finally:
        try: os.unlink(tmp_path)
        except: pass
    return None

# ── Chrome launcher ────────────────────────────────────────────────────────
def launch_chrome() -> None:
    """
    Open Google Chrome using macOS `open` command.
    If Chrome is already open, this brings it to the foreground.
    """
    log("[OS] Launching Chrome...")
    subprocess.Popen(["open", "-a", "Google Chrome"])
    time.sleep(2.5)  # wait for Chrome to come to foreground
    log("[OS] Chrome launched.")


def bring_chrome_to_front() -> None:
    """Activate Chrome if it's already open but not focused."""
    subprocess.run(
        ["osascript", "-e", 'tell application "Google Chrome" to activate'],
        capture_output=True
    )
    time.sleep(0.8)


# ── Profile selection ──────────────────────────────────────────────────────
def select_profile_vlm(target_email: str, vlm_decide_fn) -> bool:
    """
    Use the VLM to find and click the correct Chrome profile.
    
    Params:
        target_email: e.g. "swapnilhgf@gmail.com"
        vlm_decide_fn: callable(goal: str) → dict with action + x,y coords
    
    Returns True if profile was clicked, False if not found.
    """
    log(f"[OS] Looking for Chrome profile: {target_email}")

    goal = (
        f"I can see a Chrome profile picker or Chrome is open. "
        f"Find the profile for '{target_email}' and click on it. "
        f"If Chrome shows a 'Who's using Chrome?' screen with profile avatars, "
        f"click the one matching '{target_email}'. "
        f"If Chrome is already on the main window (no profile picker), "
        f"respond with action=already_open. "
        f"Respond with action=click and x,y coordinates of the profile to click."
    )

    for attempt in range(5):
        action = vlm_decide_fn(goal)
        action_type = action.get("action", "unknown")

        if action_type == "already_open":
            log("[OS] Chrome already on main window, no profile selection needed.")
            return True

        if action_type == "click":
            vx = int(action.get("x", 0))
            vy = int(action.get("y", 0))
            if vx > 0 and vy > 0:
                click(vx, vy)
                log(f"[OS] Clicked profile at ({vx}, {vy})")
                time.sleep(2.0)
                return True

        log(f"[OS] Profile selection attempt {attempt+1}: got action={action_type}, retrying...")
        time.sleep(1.5)

    log("[OS] WARNING: Could not select profile via VLM. Continuing anyway.")
    return False


# ── Navigation ─────────────────────────────────────────────────────────────
def navigate(url: str, wait_sec: float = 2.5) -> None:
    log(f"[OS] Navigating to: {url}")
    bring_chrome_to_front()
    time.sleep(0.4)

    # Click directly on the address bar (always at top of Chrome window)
    # Address bar is roughly at y=70 on a standard Chrome window, centered
    sw, sh = get_screen_size()
    bar_x = sw // 2
    bar_y = 55
    pyautogui.click(bar_x, bar_y)
    time.sleep(0.3)

    # Select all existing text and replace with new URL
    pyautogui.hotkey("command", "a")
    time.sleep(0.1)
    pyautogui.typewrite(url, interval=0.04)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(wait_sec)
    log(f"[OS] Navigation complete.")


# ── Mouse actions ───────────────────────────────────────────────────────────
def click(vx: int, vy: int, button: str = "left") -> None:
    bring_chrome_to_front()
    time.sleep(0.15)
    x, y = _scale_coords(vx, vy)
    pyautogui.moveTo(x, y, duration=0.25)
    time.sleep(0.08)
    pyautogui.click(x, y, button=button)
    log(f"[OS] Clicked ({vx},{vy}) → screen ({x},{y})")


def double_click(vx: int, vy: int) -> None:
    x, y = _scale_coords(vx, vy)
    pyautogui.moveTo(x, y, duration=0.2)
    time.sleep(0.05)
    pyautogui.doubleClick(x, y)


def scroll(direction: str = "down", amount: int = 3) -> None:
    """Scroll the current page."""
    delta = -amount if direction == "down" else amount
    pyautogui.scroll(delta)
    time.sleep(0.4)


# ── Keyboard actions ────────────────────────────────────────────────────────
def type_text(text: str, interval: float = 0.055) -> None:
    bring_chrome_to_front()
    time.sleep(0.3)
    try:
        import pyperclip
        pyperclip.copy(text)
        time.sleep(0.1)
        pyautogui.hotkey("command", "v")
        time.sleep(0.3)
    except ImportError:
        pyautogui.typewrite(text, interval=interval)


def press_enter() -> None:
    pyautogui.press("enter")
    time.sleep(0.5)


def press_escape() -> None:
    pyautogui.press("escape")
    time.sleep(0.3)


def press_tab() -> None:
    pyautogui.press("tab")
    time.sleep(0.2)


# ── Full startup sequence ───────────────────────────────────────────────────
def open_chrome_with_profile(
    target_email: str,
    vlm_decide_fn,
    start_url: str = "https://www.google.com",
) -> bool:
    """
    Complete sequence:
      1. Launch / bring Chrome to front
      2. Select the right profile (VLM-guided)
      3. Navigate to start_url
    
    Returns True on success.
    """
    log(f"[OS] Starting Chrome setup for profile: {target_email}")

    launch_chrome()

    # Give Chrome time to show profile picker (if first launch)
    time.sleep(1.5)

    # Try to select the right profile
    select_profile_vlm(target_email, vlm_decide_fn)

    # Navigate to starting URL
    navigate(start_url)

    log("[OS] Chrome ready.")
    return True


if __name__ == "__main__":
    # Quick smoke test — just launches Chrome
    launch_chrome()
    print("[os_browser] Chrome launched. Check your screen.")