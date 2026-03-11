# agent/logger.py
import os
import json
import base64
from datetime import datetime
from pathlib import Path
from agent.config import DATA_DIR

# ── Session state ─────────────────────────────────────────────────────────────
_session: dict | None = None


def start_session(goal: str) -> dict:
    """Call once at the start of each run(). Creates the session folder."""
    global _session
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = DATA_DIR / "logs" / ts
    folder.mkdir(parents=True, exist_ok=True)

    _session = {
        "goal": goal,
        "folder": folder,
        "step": 0,
        "start_time": datetime.now(),
        "log_path": folder / "session.log",
        "events": [],  # list of step dicts — written to session.json at end
    }

    _write_line("=" * 60)
    _write_line(f"SESSION START")
    _write_line(f"Goal    : {goal}")
    _write_line(f"Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    _write_line(f"Folder  : {folder}")
    _write_line("=" * 60)

    return _session


def end_session(final_state: dict) -> None:
    """Call at the end of run(). Writes summary and session.json."""
    if not _session:
        return
    duration = (datetime.now() - _session["start_time"]).total_seconds()
    _write_line("")
    _write_line("=" * 60)
    _write_line(f"SESSION END")
    _write_line(f"Steps   : {final_state.get('steps_taken', '?')}")
    _write_line(f"Done    : {final_state.get('done', '?')}")
    _write_line(f"Duration: {duration:.1f}s")
    _write_line("=" * 60)

    # Write full structured log as JSON for later analysis
    summary = {
        "goal": _session["goal"],
        "steps_taken": final_state.get("steps_taken"),
        "done": final_state.get("done"),
        "duration_s": round(duration, 1),
        "steps": _session["events"],
    }
    json_path = _session["folder"] / "session.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"[Logger] Full log saved → {_session['folder']}")


def log_step_start(step: int, goal: str) -> None:
    _session["step"] = step
    _write_line("")
    _write_line(f"┌── STEP {step} {'─' * 50}")
    _write_line(f"│  Goal: {goal}")
    _append_event({"step": step, "goal": goal})


def log_screenshot(b64: str, label: str = "screenshot") -> str:
    """Save screenshot to disk. Returns the file path."""
    if not _session:
        return ""
    step = _session["step"]
    fname = f"step_{step:03d}_{label}.jpg"
    fpath = _session["folder"] / fname

    # Decode base64 and save as JPEG
    img_bytes = base64.b64decode(b64)
    with open(fpath, "wb") as f:
        f.write(img_bytes)

    _write_line(f"│  📸 {label}: {fname}")
    _current_event()["screenshot_" + label] = fname
    return str(fpath)


def log_llm_decision(response) -> None:
    """Log what the LLM decided to do."""
    if not _session:
        return

    tool_calls = getattr(response, "tool_calls", [])
    content = getattr(response, "content", "")

    if tool_calls:
        for tc in tool_calls:
            name = tc.get("name", "?")
            args = tc.get("args", {})
            _write_line(f"│  🧠 LLM decided → {name}({_fmt_args(args)})")
            _current_event()["llm_decision"] = {
                "tool": name,
                "args": args,
            }
    elif content:
        _write_line(f"│  🧠 LLM response (no tool call): {content[:200]}")
        _current_event()["llm_decision"] = {"raw": content}
    else:
        _write_line(f"│  🧠 LLM: no tool call and no content")
        _current_event()["llm_decision"] = None


def log_tool_execution(name: str, args: dict, result: str) -> None:
    """Log what tool ran and what it returned."""
    if not _session:
        return
    _write_line(f"│  🖱️  Executed: {name}({_fmt_args(args)})")
    _write_line(f"│  ↳  Result  : {result}")
    _current_event()["tool_executed"] = {
        "name": name,
        "args": args,
        "result": result,
    }


def log_verification(success: bool, reason: str, suggestion: str = "") -> None:
    """Log the verification result after each action."""
    if not _session:
        return
    icon = "✓" if success else "✗"
    _write_line(f"│  {icon} Verify: {reason}")
    if suggestion:
        _write_line(f"│  💡 Suggestion: {suggestion}")
    _current_event()["verification"] = {
        "success": success,
        "reason": reason,
        "suggestion": suggestion,
    }


def log_retry(retry: int, max_retries: int, hint: str) -> None:
    if not _session:
        return
    _write_line(f"│  ⚠️  Retry {retry}/{max_retries}: {hint}")


def log_step_end() -> None:
    _write_line(f"└── END STEP {_session['step']} {'─' * 46}")


def log(message: str) -> None:
    """Write to session log file and print to terminal once."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {message}"
    
    # Print to terminal
    print(line)
    
    # Write to file
    if _session and _session.get("log_path"):
        with open(_session["log_path"], "a") as f:
            f.write(line + "\n")


# ── Internals ──────────────────────────────────────────────────────────────────
def _write_line(line: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    full = f"[{ts}] {line}"
    print(full, flush=True)
    if _session:
        with open(_session["log_path"], "a", encoding="utf-8") as f:
            f.write(full + "\n")


def _append_event(event: dict) -> None:
    if _session is not None:
        _session["events"].append(event)


def _current_event() -> dict:
    """Return the most recent event dict so nodes can add fields to it."""
    if _session and _session["events"]:
        return _session["events"][-1]
    e = {}
    _session["events"].append(e)
    return e


def _fmt_args(args: dict) -> str:
    parts = []
    for k, v in args.items():
        val = f'"{v}"' if isinstance(v, str) else str(v)
        parts.append(f"{k}={val}")
    return ", ".join(parts)
