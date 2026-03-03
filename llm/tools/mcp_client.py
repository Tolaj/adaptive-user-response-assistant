# llm/tools/mcp_client.py


# ─────────────────────────────────────────────
# NEW: llm/tools/mcp_client.py
# Runs apple-mcp as a subprocess, keeps the
# async session alive in a background thread,
# exposes a plain sync call_tool() so the rest
# of AURA never touches async.
# ─────────────────────────────────────────────
import asyncio
import threading

_loop: asyncio.AbstractEventLoop | None = None
_session = None
_shutdown_event = None  # asyncio.Event, set from _loop thread
_ready = threading.Event()  # set when session is initialised
_start_lock = threading.Lock()
_thread = None


async def _main(ready: threading.Event) -> None:
    global _session, _shutdown_event
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    _shutdown_event = asyncio.Event()
    params = StdioServerParameters(command="npx", args=["apple-mcp"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            _session = session
            ready.set()
            await _shutdown_event.wait()  # keep context managers alive


def _thread_fn() -> None:
    global _loop
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(_main(_ready))


def ensure_started() -> None:
    global _thread
    with _start_lock:
        if _thread is not None:
            return
        import subprocess, time

        subprocess.run(["open", "-a", "Messages"], capture_output=True)
        subprocess.run(["open", "-a", "Contacts"], capture_output=True)
        time.sleep(1.5)
        _thread = threading.Thread(target=_thread_fn, daemon=True, name="mcp-client")
        _thread.start()
    if not _ready.wait(timeout=20):
        print("[MCP] Warning: apple-mcp did not start in time")


def call_tool(name: str, args: dict) -> str:
    ensure_started()
    if _session is None:
        return "[MCP] Session not ready"
    future = asyncio.run_coroutine_threadsafe(_session.call_tool(name, args), _loop)
    try:
        result = future.result(timeout=15)
        parts = [b.text for b in result.content if hasattr(b, "text")]
        return "\n".join(parts) if parts else "Done."
    except Exception as e:
        import traceback

        traceback.print_exc()
        return f"[MCP error] {e}"


def shutdown() -> None:
    if _loop and _shutdown_event:
        _loop.call_soon_threadsafe(_shutdown_event.set)
