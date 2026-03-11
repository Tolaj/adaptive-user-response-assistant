# agent/controls.py
import time
import subprocess
import pyautogui
from agent.snap import get_screen_size, SNAP_WIDTH, SNAP_HEIGHT
from agent.logger import log
from agent.config import CLICK_OFFSET_X, CLICK_OFFSET_Y

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05


def _scale_coords(vx: int, vy: int) -> tuple[int, int]:
    sw, sh = get_screen_size()
    sx = int(vx * sw / SNAP_WIDTH)  + CLICK_OFFSET_X
    sy = int(vy * sh / SNAP_HEIGHT) + CLICK_OFFSET_Y
    # Clamp to screen bounds
    sx = max(0, min(sw, sx))
    sy = max(0, min(sh, sy))
    return sx, sy


# ── Chrome ──────────────────────────────────────────────────────────────────
def launch_chrome() -> None:
    log("[Controls] Launching Chrome...")
    subprocess.Popen(["open", "-a", "Google Chrome"])
    time.sleep(2.5)


def bring_chrome_to_front() -> None:
    subprocess.run(
        ["osascript", "-e", 'tell application "Google Chrome" to activate'],
        capture_output=True,
    )
    time.sleep(0.8)


def navigate(url: str, wait_sec: float = 2.5) -> None:
    log(f"[Controls] Navigating to: {url}")
    bring_chrome_to_front()
    time.sleep(0.4)
    sw, sh = get_screen_size()
    pyautogui.click(sw // 2, 55)
    time.sleep(0.3)
    pyautogui.hotkey("command", "a")
    time.sleep(0.1)
    pyautogui.typewrite(url, interval=0.04)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(wait_sec)


# ── Mouse ───────────────────────────────────────────────────────────────────
def click(vx: int, vy: int, button: str = "left") -> None:
    bring_chrome_to_front()
    time.sleep(0.15)
    x, y = _scale_coords(vx, vy)
    pyautogui.moveTo(x, y, duration=0.25)
    time.sleep(0.08)
    pyautogui.click(x, y, button=button)
    log(f"[Controls] Clicked ({vx},{vy}) → screen ({x},{y})")


def double_click(vx: int, vy: int) -> None:
    x, y = _scale_coords(vx, vy)
    pyautogui.moveTo(x, y, duration=0.2)
    time.sleep(0.05)
    pyautogui.doubleClick(x, y)


def scroll(direction: str = "down", amount: int = 3) -> None:
    delta = -amount if direction == "down" else amount
    pyautogui.scroll(delta)
    time.sleep(0.4)


# ── Keyboard ─────────────────────────────────────────────────────────────────
def type_text(text: str) -> None:
    bring_chrome_to_front()
    time.sleep(0.3)
    try:
        import pyperclip

        pyperclip.copy(text)
        time.sleep(0.1)
        pyautogui.hotkey("command", "v")
        time.sleep(0.3)
    except ImportError:
        pyautogui.typewrite(text, interval=0.055)


def press_enter() -> None:
    pyautogui.press("enter")
    time.sleep(0.5)


def press_escape() -> None:
    pyautogui.press("escape")
    time.sleep(0.3)


def press_tab() -> None:
    pyautogui.press("tab")
    time.sleep(0.2)


def hotkey(*keys: str) -> None:
    pyautogui.hotkey(*keys)
    time.sleep(0.5)
