# PromptPack Output

**Root:** `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/agent`
**Generated:** 2026-03-10T17:48:22.472Z

---

## 1) Folder Structure

```txt
.
├─ __init__.py
├─ config.py
├─ controls.py
├─ executor.py
├─ logger.py
├─ snap.py
└─ tools/
   └─ __init__.py
```

<!-- PAGE BREAK: FILE CONTENTS BELOW -->

## 2) File Contents


### __init__.py

```python
# agent/__init__.py

from agent.snap import snap_screen_b64
from agent.controls import (
    launch_chrome,
    bring_chrome_to_front,
    navigate,
    click,
    type_text,
    scroll,
    press_enter,
    find_text_on_screen,
)
from agent.executor import decide_action, execute_action
from agent.logger import log

```

### config.py

```python
# agent/config.py
# ─────────────────────────────────────────────────────────────────────────────
# Job hunter runtime configuration — tweak these without touching core logic
# ─────────────────────────────────────────────────────────────────────────────

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "jobs.db"
CSV_PATH = DATA_DIR / "jobs_found.csv"
LOG_PATH = DATA_DIR / "agent.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Scheduler ─────────────────────────────────────────────────────────────
RUN_EVERY_HOURS = 2  # how often the full hunt cycle runs

# ── VLM settings (mirrors your config/vlm.py style) ──────────────────────
VLM_SERVER_PORT = 8081  # must match your config/vlm.py VLM_SERVER_PORT
VLM_MAX_TOKENS = 120  # slightly more than vision assistant — needs JSON
VLM_TEMPERATURE = 0.1  # low = consistent, deterministic action decisions

# ── Agent loop limits ──────────────────────────────────────────────────────
MAX_ACTIONS_PER_PAGE = 40  # max VLM → click/type steps before giving up
MAX_JOBS_PER_SITE = 20  # stop scrolling after collecting this many
ACTION_DELAY_MS = 1500  # ms to wait after each action (human-like)
PAGE_LOAD_WAIT_MS = 2500  # ms to wait after navigation

# ── Screenshot settings (mirrors your config/vlm.py camera settings) ──────
SCREENSHOT_WIDTH = 1280
SCREENSHOT_HEIGHT = 800
JPEG_QUALITY = 75  # higher than camera — need to read text clearly

# ── Scoring thresholds ─────────────────────────────────────────────────────
MIN_SCORE_TO_SAVE = 5  # VLM scores 1–10; only save jobs >= this score

```

### controls.py

```python
# agent/controls.py
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
from agent.snap import snap_screen_b64, get_screen_size, SNAP_WIDTH, SNAP_HEIGHT
from agent.logger import log

# Safety: pyautogui raises exception if mouse hits screen corner
pyautogui.FAILSAFE = True
# Small pause between pyautogui actions to feel human
pyautogui.PAUSE = 0.05


# ── Coordinate scaling ─────────────────────────────────────────────────────
def _scale_coords(vx: int, vy: int) -> tuple[int, int]:
    sw, sh = get_screen_size()
    vx = max(0, min(vx, 640))
    vy = max(0, min(vy, 400))
    x = int((640 - vx) * sw / 640)  # mirror x back
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
        subprocess.run(
            ["screencapture", "-x", tmp_path], check=True, capture_output=True
        )
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
        try:
            os.unlink(tmp_path)
        except:
            pass
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
        capture_output=True,
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

        log(
            f"[OS] Profile selection attempt {attempt+1}: got action={action_type}, retrying..."
        )
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

```

### executor.py

```python
# agent/executor.py
# ─────────────────────────────────────────────────────────────────────────────
# VLM-guided OS automation actions.
# Replaces agent/actions.py (which used Playwright).
# Takes a real screenshot → asks your VLM → executes via pyautogui.
#
# Usage:
#   from agent.executor import decide_and_execute, os_navigate
# ─────────────────────────────────────────────────────────────────────────────

import json
import re
import time
import requests

from agent.snap import snap_screen_b64
from agent.controls import (
    click,
    double_click,
    scroll,
    type_text,
    press_enter,
    press_escape,
    navigate,
    bring_chrome_to_front,
)
from agent.config import VLM_SERVER_PORT, VLM_MAX_TOKENS, VLM_TEMPERATURE
from agent.logger import log


# ── VLM system prompts ──────────────────────────────────────────────────────
_NAV_SYSTEM = """You are a browser automation agent controlling a REAL macOS Chrome browser via mouse and keyboard.
You see a screenshot of the current screen.
Your job is to take ONE action to make progress toward the goal.

You MUST respond with ONLY a JSON object — no explanation, no markdown.

JSON format:
{
  "action": "click" | "type" | "scroll" | "wait" | "extract" | "done" | "navigate" | "already_open" | "press_enter" | "hotkey",
  "x": <pixel x in 1280x800 space, only for click>,
  "y": <pixel y in 1280x800 space, only for click>,
  "text": "<text to type, only for type action>",
  "url": "<url, only for navigate action>",
  "keys": "<hotkey combo like 'command+l', only for hotkey action>",
  "direction": "down" | "up",
  "reason": "<one short sentence why>"
}

IMPORTANT coordinate rules:
- The screenshot is 1280x800 pixels
- x=0 is LEFT edge, x=1280 is RIGHT edge
- y=0 is TOP edge, y=800 is BOTTOM edge
- Be precise — click the CENTER of buttons/links/input fields
"""

_EXTRACT_SYSTEM = """You are a job listing extractor. You see a screenshot of a job search results page.
Extract ALL visible job listings into a JSON array.
Respond with ONLY a JSON array — no markdown, no explanation.

Each item:
{
  "title": "<job title>",
  "company": "<company name>",
  "location": "<location or Remote>",
  "salary": "<salary if shown, else null>",
  "posted": "<time posted if shown, else null>",
  "url": "<job URL if visible, else null>",
  "snippet": "<brief description if visible, else null>"
}

If no job listings visible, return: []
"""

_LOGIN_SYSTEM = """You are helping automate a browser login flow on macOS Chrome.
You see a screenshot. Identify what login step is currently visible and what to click/type next.

Respond with ONLY a JSON object:
{
  "action": "click" | "type" | "press_enter" | "done" | "wait",
  "x": <x in 1280x800 space>,
  "y": <y in 1280x800 space>,
  "text": "<text to type if action=type>",
  "step": "<what step you see: profile_picker | email_input | password_input | signed_in | captcha | 2fa | other>",
  "reason": "<one sentence>"
}
"""


# ── Core VLM call ───────────────────────────────────────────────────────────
def _call_vlm(
    screenshot_b64: str, system_prompt: str, user_prompt: str, max_tokens: int = None
) -> str:
    """Single HTTP call to llama-server."""
    try:
        response = requests.post(
            f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{screenshot_b64}"
                                },
                            },
                            {"type": "text", "text": user_prompt},
                        ],
                    },
                ],
                "max_tokens": max_tokens or VLM_MAX_TOKENS,
                "temperature": VLM_TEMPERATURE,
                "stream": False,
            },
            timeout=30,
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log(f"[VLM] Call failed: {e}")
        try:
            log(f"[VLM] Raw response: {response.json()}")
        except:
            pass
        return "{}"


def _parse_json(raw: str) -> dict | list:
    """Robustly extract JSON from VLM response."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r"(\{.*\}|\[.*\])", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return {}


# ── Action execution ────────────────────────────────────────────────────────
def execute_action(action: dict) -> str:
    """Execute a VLM action dict using real OS controls."""
    action_type = action.get("action", "unknown")

    try:
        if action_type == "click":
            vx = action.get("x", 0)
            vy = action.get("y", 0)
            # VLM sometimes returns x as [x, y] list — handle it
            if isinstance(vx, list):
                vx, vy = vx[0], vx[1]
            click(int(vx), int(vy))
            time.sleep(0.8)

        elif action_type == "double_click":
            vx = int(action.get("x", 0))
            vy = int(action.get("y", 0))
            double_click(vx, vy)
            time.sleep(0.8)

        elif action_type == "type":
            text = action.get("text", "")
            if text:
                type_text(text)
                time.sleep(0.4)

        elif action_type == "press_enter":
            press_enter()

        elif action_type == "hotkey":
            import pyautogui

            keys = action.get("keys", "").replace("+", " ").split()
            if keys:
                pyautogui.hotkey(*keys)
                time.sleep(0.5)

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            scroll(direction, amount=3)

        elif action_type == "navigate":
            url = action.get("url", "")
            if url:
                navigate(url)

        elif action_type == "wait":
            time.sleep(2.0)

        elif action_type in ("extract", "done", "already_open"):
            pass  # handled by caller

        else:
            log(f"[OS Actions] Unknown action: {action_type}")

    except Exception as e:
        log(f"[OS Actions] Failed to execute {action_type}: {e}")

    return action_type


# ── High-level helpers ──────────────────────────────────────────────────────
def decide_action(goal: str) -> dict:
    from jobhunter.os_browser import bring_chrome_to_front

    bring_chrome_to_front()
    time.sleep(0.4)
    screenshot = snap_screen_b64()
    prompt = f"Goal: {goal}\n\nWhat is the single next action? Respond in JSON only."
    raw = _call_vlm(screenshot, _NAV_SYSTEM, prompt)
    action = _parse_json(raw)
    log(f"[VLM→Action] {action.get('action','?')} — {action.get('reason','')}")
    return action if isinstance(action, dict) else {}


def decide_login_step() -> dict:
    """Screenshot → VLM → login step dict."""
    screenshot = snap_screen_b64()
    prompt = "What login step is currently visible? What should I do next?"
    raw = _call_vlm(screenshot, _LOGIN_SYSTEM, prompt, max_tokens=150)
    result = _parse_json(raw)
    log(f"[VLM→Login] step={result.get('step','?')} action={result.get('action','?')}")
    return result if isinstance(result, dict) else {}


def extract_jobs_from_screen() -> list[dict]:
    """Screenshot → VLM → list of job dicts."""
    screenshot = snap_screen_b64()
    prompt = "Extract all visible job listings from this screenshot as a JSON array."
    raw = _call_vlm(screenshot, _EXTRACT_SYSTEM, prompt, max_tokens=500)
    result = _parse_json(raw)
    jobs = result if isinstance(result, list) else []
    log(f"[VLM→Extract] Found {len(jobs)} jobs on screen")
    return jobs


def os_navigate(url: str) -> None:
    """Navigate Chrome to URL using keyboard (no Playwright)."""
    navigate(url)

```

### logger.py

```python
# agent/logger.py
# ─────────────────────────────────────────────────────────────────────────────
# Simple file + console logger. Mirrors server/logger.py style.
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime
from agent.config import LOG_PATH


def log(message: str) -> None:
    """Print to console and append to log file."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # never crash because of logging

```

### snap.py

```python
# agent/snap.py
# ─────────────────────────────────────────────────────────────────────────────
# macOS screen capture → base64 JPEG
# Uses native screencapture — no Playwright, no OpenCV dependency for screen.
# Drop-in replacement for agent/snap.py but captures the REAL screen.
# ─────────────────────────────────────────────────────────────────────────────

import base64
import subprocess
import tempfile
import os
from PIL import Image
import io

# Resolution to send to VLM — big enough to read text, small enough to be fast
SNAP_WIDTH = 640
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
        subprocess.run(
            ["screencapture", "-x", "-1", tmp_path], check=True, capture_output=True
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
        return (2560, 1600)  # safe fallback for Retina MacBook


if __name__ == "__main__":
    b64 = snap_screen_b64()
    print(f"[os_snap] Screenshot captured: {len(b64)} base64 chars")

```

### tools/__init__.py

```python


```