# llm/tools/executor.py


# ─────────────────────────────────────────────
# NEW: llm/tools/executor.py
# Routes Qwen's tool_call name → correct
# apple-mcp tool + args, or local search.
# ─────────────────────────────────────────────
from llm.tools.search import web_search
from llm.tools.mcp_client import call_tool
import re, subprocess


def _resolve_contact_and_send(args: dict) -> dict:
    import re, subprocess

    name = args.get("phoneNumber", "")
    if name and not any(c.isdigit() for c in name):
        number = _get_number_via_applescript(name)
        print(f"[DEBUG] resolved '{name}' → '{number}'")  # already there
        print(f"[DEBUG] cleaned number: '{_clean_number(number)}'")  # add this
        if number:
            args = {**args, "phoneNumber": _clean_number(number)}
    return {"operation": "send", **args}


def _clean_number(number: str) -> str:
    import re

    digits = re.sub(r"\D", "", number)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return number


def _get_number_via_applescript(name: str) -> str:
    script = f"""
tell application "Contacts"
    try
        set p to first person whose name contains "{name}"
        return value of first phone of p
    on error
        return ""
    end try
end tell
"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[AppleScript] {e}")
        return ""


def execute(name: str, args: dict) -> str:
    if name == "search_web":
        return web_search(args.get("query", ""))

    _MAP = {
        "send_imessage": ("messages", lambda a: _resolve_contact_and_send(a)),
        "read_imessage": ("messages", lambda a: {"operation": "read", **a}),
        "unread_imessages": ("messages", lambda a: {"operation": "unread", **a}),
        "create_reminder": ("reminders", lambda a: {"operation": "create", **a}),
        "list_reminders": ("reminders", lambda a: {"operation": "list"}),
        "create_calendar_event": ("calendar", lambda a: {"operation": "create", **a}),
        "list_calendar_events": ("calendar", lambda a: {"operation": "list", **a}),
        "search_contacts": ("contacts", lambda a: a),
    }

    if name not in _MAP:
        return f"[Executor] Unknown tool: {name}"

    mcp_tool, build_args = _MAP[name]
    return call_tool(mcp_tool, build_args(args))
