# agent/loop.py
# ─────────────────────────────────────────────────────────────────────────────
# Core screen agent loop.
#
# Perception:  _snap_screen_pil()          → PIL image  (no jobhunter dep)
# Parsing:     OmniParser.parse()          → annotated PIL + element list
# Reasoning:   Local VLM server            → JSON action
# Execution:   pyautogui                   → mouse + keyboard
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import base64
import json
import re
import time
import subprocess
from io import BytesIO
from typing import Optional

import pyautogui
import requests
from PIL import Image

from config.vlm import VLM_SERVER_PORT
from config.agent import (
    AGENT_MAX_STEPS,
    AGENT_STEP_DELAY,
    AGENT_MAX_TOKENS,
    AGENT_TEMPERATURE,
)
from agent.prompt import AGENT_SYSTEM_PROMPT
from agent.tools.omniparser import parse as omniparse, elements_to_text


# ── Logging (no jobhunter dep) ─────────────────────────────────────────────
def _log(msg: str) -> None:
    print(msg, flush=True)


# ── Screen capture (replaces jobhunter.os_snap) ────────────────────────────
def _snap_screen_pil() -> Image.Image:
    """Capture full screen as PIL Image. Works on macOS, Linux, Windows."""
    return pyautogui.screenshot()


# ── Mouse / keyboard helpers (replaces jobhunter.os_browser) ──────────────
def _click(x: int, y: int) -> None:
    pyautogui.click(x, y)
    time.sleep(0.15)


def _double_click(x: int, y: int) -> None:
    pyautogui.doubleClick(x, y)
    time.sleep(0.15)


def _type_text(text: str, interval: float = 0.04) -> None:
    pyautogui.typewrite(text, interval=interval)


def _press_enter() -> None:
    pyautogui.press("enter")


def _scroll(direction: str, amount: int = 3, x: int = None, y: int = None) -> None:
    clicks = amount if direction == "up" else -amount
    if x is not None and y is not None:
        pyautogui.scroll(clicks, x=x, y=y)
    else:
        pyautogui.scroll(clicks)


# ── Helpers ────────────────────────────────────────────────────────────────
def _pil_to_b64(img: Image.Image, quality: int = 70) -> str:
    buf = BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return {}


# ── VLM call ────────────────────────────────────────────────────────────────
def _ask_vlm(
    annotated_img: Image.Image,
    element_text: str,
    goal: str,
    history: list[str],
) -> dict:
    history_text = "\n".join(history[-8:]) if history else "None yet."

    user_content = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{_pil_to_b64(annotated_img)}"
            },
        },
        {
            "type": "text",
            "text": (
                f"GOAL: {goal}\n\n"
                f"ACTION HISTORY (most recent last):\n{history_text}\n\n"
                f"{element_text}\n\n"
                "Output your next action as JSON:"
            ),
        },
    ]

    try:
        response = requests.post(
            f"http://localhost:{VLM_SERVER_PORT}/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                "max_tokens": AGENT_MAX_TOKENS,
                "temperature": AGENT_TEMPERATURE,
                "stream": False,
            },
            timeout=30,
        )
        raw = response.json()["choices"][0]["message"]["content"].strip()
        action = _parse_json(raw)
        _log(f"[Agent] VLM → {action.get('action','?')}  {action}")
        return action
    except Exception as e:
        _log(f"[Agent] VLM call failed: {e}")
        return {}


# ── Action executor ────────────────────────────────────────────────────────
def _execute(action: dict) -> bool:
    """Execute one action. Returns True if agent should stop (done/error)."""
    t = action.get("action", "unknown")

    try:
        if t == "click":
            _click(int(action["x"]), int(action["y"]))

        elif t == "double_click":
            _double_click(int(action["x"]), int(action["y"]))

        elif t == "right_click":
            pyautogui.rightClick(int(action["x"]), int(action["y"]))

        elif t == "type":
            # Click position first if provided, then type
            if "x" in action and "y" in action:
                _click(int(action["x"]), int(action["y"]))
            _type_text(str(action["text"]))

        elif t == "key":
            keys = action.get("keys", [])
            if isinstance(keys, str):
                keys = keys.replace("+", " ").split()
            pyautogui.hotkey(*keys)
            time.sleep(0.3)

        elif t == "scroll":
            direction = action.get("direction", "down")
            amount = int(action.get("amount", 3))
            x = action.get("x")
            y = action.get("y")
            _scroll(direction, amount=amount, x=x, y=y)

        elif t == "wait":
            time.sleep(float(action.get("seconds", 1.0)))

        elif t == "screenshot":
            # Agent requested a fresh look — no-op, next iteration re-perceives
            _log("[Agent] Re-perceiving screen...")

        elif t == "done":
            _log(f"[Agent] Done — {action.get('reason', '')}")
            return True

        else:
            _log(f"[Agent] Unknown action '{t}' — skipping.")

    except Exception as e:
        _log(f"[Agent] Execute error ({t}): {e}")

    return False


# ── Main agent ─────────────────────────────────────────────────────────────
class ScreenAgent:
    """
    Pure-vision screen agent.

    Perception:  pyautogui screenshot + OmniParser
    Reasoning:   Local Qwen3-VL via llama-server
    Execution:   pyautogui (mouse + keyboard)
    No OS APIs, no MCP, no Playwright, no jobhunter dependency.
    """

    def __init__(self):
        _log("[Agent] Initialising OmniParser...")
        from agent.tools.omniparser import _get_parser

        _get_parser()
        _log("[Agent] Ready.")

    def _perceive(self) -> tuple[Image.Image, list[dict]]:
        """Take screenshot → OmniParser → (annotated_img, elements)."""
        img = _snap_screen_pil()
        annotated, elements = omniparse(img)
        _log(f"[Agent] Perceived {len(elements)} elements on screen.")
        return annotated, elements

    def run(self, goal: str, focus_app: Optional[str] = None) -> None:
        """
        Run the agent until the goal is done or max steps reached.

        Parameters
        ----------
        goal        : Natural language task description
        focus_app   : Optional macOS app name to bring to front first
                      e.g. "Messages", "Finder", "Google Chrome"
        """
        _log(f"\n[Agent] ═══════════════════════════════════")
        _log(f"[Agent] Goal: {goal}")
        _log(f"[Agent] ═══════════════════════════════════")

        if focus_app:
            try:
                subprocess.run(
                    ["osascript", "-e", f'tell application "{focus_app}" to activate'],
                    capture_output=True,
                )
                time.sleep(0.8)
            except Exception as e:
                _log(f"[Agent] Could not focus app '{focus_app}': {e}")

        history: list[str] = []

        for step in range(1, AGENT_MAX_STEPS + 1):
            _log(f"\n[Agent] ── Step {step}/{AGENT_MAX_STEPS} ──")

            # 1. Perceive
            annotated, elements = self._perceive()
            element_text = elements_to_text(elements)

            # 2. Reason
            action = _ask_vlm(annotated, element_text, goal, history)
            if not action:
                _log("[Agent] Empty action from VLM — retrying in 2s...")
                time.sleep(2)
                continue

            history.append(f"Step {step}: {json.dumps(action)}")

            # 3. Act
            done = _execute(action)
            if done:
                break

            time.sleep(AGENT_STEP_DELAY)

        else:
            _log(f"[Agent] Reached max steps ({AGENT_MAX_STEPS}).")

        _log("[Agent] Run complete.")
