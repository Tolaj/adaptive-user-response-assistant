import threading
import sys
import tty
import termios
from pynput import keyboard

_pressed = False
_listener = None
_on_press_cb = None
_on_release_cb = None


def _on_press(key):
    global _pressed
    if key == keyboard.Key.space and not _pressed:
        _pressed = True
        if _on_press_cb:
            _on_press_cb()


def _on_release(key):
    global _pressed
    if key == keyboard.Key.space and _pressed:
        _pressed = False
        if _on_release_cb:
            _on_release_cb()


def start_ptt(on_press, on_release):
    global _listener, _on_press_cb, _on_release_cb
    _on_press_cb = on_press
    _on_release_cb = on_release

    # Suppress terminal echo so SPACE doesn't move the cursor
    if sys.stdin.isatty():
        fd = sys.stdin.fileno()
        attrs = termios.tcgetattr(fd)
        attrs[3] &= ~termios.ECHO   # turn off echo
        termios.tcsetattr(fd, termios.TCSANOW, attrs)

    _listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
    _listener.start()
    print("  🎙️  Push-to-talk enabled — hold SPACE to speak")


def stop_ptt():
    global _listener
    if _listener:
        _listener.stop()
        _listener = None

    # Restore terminal echo
    if sys.stdin.isatty():
        fd = sys.stdin.fileno()
        attrs = termios.tcgetattr(fd)
        attrs[3] |= termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, attrs)


def is_pressed() -> bool:
    return _pressed