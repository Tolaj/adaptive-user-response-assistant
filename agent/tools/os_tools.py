# agent/tools/os_tools.py
import time
from typing import Literal, Annotated
from langchain_core.tools import tool
from pydantic import Field


@tool
def click(
    x: Annotated[int, Field(description="X coordinate in 640x400 screenshot space")],
    y: Annotated[int, Field(description="Y coordinate in 640x400 screenshot space")],
) -> str:
    """
    Move the mouse to (x, y) and click.
    Use this to click buttons, links, input fields, icons.
    Always look at the screenshot first to confirm the element is visible.
    """
    from agent.controls import click as _click

    _click(x, y)
    time.sleep(0.8)
    return f"Moved mouse to ({x},{y}) and clicked. Verify the element responded."


@tool
def double_click(
    x: Annotated[int, Field(description="X coordinate in 640x400 screenshot space")],
    y: Annotated[int, Field(description="Y coordinate in 640x400 screenshot space")],
) -> str:
    """
    Double-click at (x, y).
    Use for opening files, selecting words, activating items.
    """
    from agent.controls import double_click as _double_click

    _double_click(x, y)
    time.sleep(0.8)
    return f"Double-clicked at ({x},{y}). Verify the item opened or was selected."


@tool
def type_text(
    text: Annotated[
        str,
        Field(description="Text to type. Make sure an input field is focused first."),
    ],
) -> str:
    """
    Type text using the keyboard.
    IMPORTANT: You must click the input field first before calling this.
    """
    from agent.controls import type_text as _type_text

    _type_text(text)
    time.sleep(0.4)
    return f"Typed '{text}'. Verify it appeared in the input field."


@tool
def scroll(
    direction: Annotated[
        Literal["down", "up"], Field(description="Which direction to scroll")
    ] = "down",
    amount: Annotated[int, Field(description="How many ticks to scroll, 1-10")] = 3,
) -> str:
    """Scroll the page up or down."""
    from agent.controls import scroll as _scroll

    _scroll(direction, amount)
    time.sleep(0.4)
    return f"Scrolled {direction} by {amount} ticks. Verify page moved."


@tool
def press_enter() -> str:
    """
    Press the Enter key.
    Use after typing in a search box or form field to submit.
    """
    from agent.controls import press_enter as _press_enter

    _press_enter()
    time.sleep(0.5)
    return "Pressed Enter. Verify the form submitted or action triggered."


@tool
def press_escape() -> str:
    """Press Escape to close a dialog, menu, or cancel an action."""
    from agent.controls import press_escape as _press_escape

    _press_escape()
    time.sleep(0.3)
    return "Pressed Escape."


@tool
def press_tab() -> str:
    """Press Tab to move focus to the next input field."""
    from agent.controls import press_tab as _press_tab

    _press_tab()
    time.sleep(0.2)
    return "Pressed Tab. Verify focus moved to next element."


@tool
def hotkey(
    keys: Annotated[
        str, Field(description="Key combo e.g. 'command+c', 'command+t', 'command+l'")
    ],
) -> str:
    """
    Press a keyboard shortcut.
    Common ones: command+t (new tab), command+l (focus address bar),
    command+c (copy), command+v (paste), command+a (select all).
    """
    from agent.controls import hotkey as _hotkey

    parts = keys.replace("+", " ").split()
    _hotkey(*parts)
    time.sleep(0.5)
    return f"Pressed hotkey '{keys}'. Verify the expected result."


@tool
def navigate(
    url: Annotated[str, Field(description="Full URL including https://")],
) -> str:
    """
    Navigate Chrome to a URL by clicking the address bar and typing.
    Use this for direct navigation to known URLs.
    """
    from agent.controls import navigate as _navigate

    _navigate(url)
    time.sleep(1.0)
    return f"Navigated to {url}. Verify the page loaded."


@tool
def mark_done(
    reason: Annotated[str, Field(description="What was accomplished")] = "",
) -> str:
    """
    Call this when the goal is fully complete.
    Only call this when you can see in the screenshot that the task is done.
    """
    return f"Task complete: {reason}"

@tool
def open_app_window(
    app_name: Annotated[str, Field(description="App name e.g. 'Messages', 'Finder', 'Safari'")],
) -> str:
    """
    Open an application and ensure a window is visible.
    Use this when goal is to open an app.
    """
    import subprocess
    import time

    # Common name aliases — user might say "iMessage" but app is "Messages"
    ALIASES = {
        "imessage":   "Messages",
        "iMessage":   "Messages",
        "chrome":     "Google Chrome",
        "vscode":     "Visual Studio Code",
        "vs code":    "Visual Studio Code",
        "terminal":   "Terminal",
        "finder":     "Finder",
        "safari":     "Safari",
        "mail":       "Mail",
        "notes":      "Notes",
        "calendar":   "Calendar",
        "messages":   "Messages",
    }

    resolved = ALIASES.get(app_name, ALIASES.get(app_name.lower(), app_name))

    try:
        # `open -a` is the most reliable way — works for every app
        result = subprocess.run(
            ["open", "-a", resolved],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return f"Failed to open {resolved}: {result.stderr.strip()}"

        time.sleep(1.5)  # wait for window to appear
        return f"Opened {resolved} successfully."

    except Exception as e:
        return f"Error: {e}"