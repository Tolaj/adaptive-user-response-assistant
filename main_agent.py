#!/usr/bin/env python3
# main_agent.py
# ─────────────────────────────────────────────────────────────────────────────
# Entry point for the general-purpose screen agent.
# Uses OmniParser for perception + local Qwen3-VL (llama-server) for reasoning.
#
# Usage:
#   python main_agent.py "Open Safari and go to github.com"
#   python main_agent.py --app Safari "Go to github.com"
#   python main_agent.py --interactive
#
# Prerequisites:
#   1. llama-server running with Qwen3-VL:
#        llama-server -m models/vlm/qwen3vl2b/Qwen3VL-2B-Instruct-Q4_K_M.gguf \
#                     --mmproj models/vlm/qwen3vl2b/mmproj-Qwen3-VL-2B-Instruct-Q8_0.gguf \
#                     -ngl 99 -c 4096 --port 8081
#      (or pass --no-vlm-start if it's already running)
#
#   2. OmniParser weights at models/omniparser/weights/:
#        git clone https://github.com/microsoft/OmniParser
#        cd OmniParser && python weights/download_weights.py
#        pip install -e .
#      Then verify OMNIPARSER_WEIGHTS_DIR in config/agent.py points there.
# ─────────────────────────────────────────────────────────────────────────────

import sys
import time
import argparse

_vlm_proc = None


def main():
    parser = argparse.ArgumentParser(
        description="Screen Agent — OmniParser + Qwen3-VL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "goal",
        nargs="*",
        help='Task to perform, e.g. "Open Safari and search for cats"',
    )
    parser.add_argument(
        "--app",
        type=str,
        default=None,
        help="macOS app to bring to front before starting (e.g. 'Messages', 'Safari')",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for tasks in a loop instead of running a single task",
    )
    parser.add_argument(
        "--no-vlm-start",
        action="store_true",
        help="Skip auto-starting the VLM server (assume it's already running)",
    )
    args = parser.parse_args()

    # ── Start VLM server if needed ─────────────────────────────────────────
    if not args.no_vlm_start:
        _start_vlm_server()

    # ── Initialise agent ───────────────────────────────────────────────────
    from agent.loop import ScreenAgent

    agent = ScreenAgent()

    # ── Interactive mode ───────────────────────────────────────────────────
    if args.interactive:
        print("\n  Screen Agent — Interactive Mode")
        print("  Type a task and press Enter. Empty line to quit.\n")
        while True:
            try:
                goal = input("  Task: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n  Bye.")
                break
            if not goal:
                break
            agent.run(goal, focus_app=args.app)
            print()
        return

    # ── Single task mode ───────────────────────────────────────────────────
    if not args.goal:
        parser.print_help()
        sys.exit(1)

    goal = " ".join(args.goal)
    agent.run(goal, focus_app=args.app)


# ── VLM server auto-start ──────────────────────────────────────────────────
def _start_vlm_server():
    """Start llama-server as a subprocess if not already running."""
    global _vlm_proc
    import requests
    import subprocess
    from config.vlm import (
        VLM_SERVER_PORT,
        VLM_SERVER_BINARY,
        VLM_MODEL_PATH,
        VLM_MMPROJ_PATH,
    )

    url = f"http://localhost:{VLM_SERVER_PORT}/health"

    # Already running?
    try:
        if requests.get(url, timeout=2).status_code == 200:
            print(f"[VLM] Server already running on port {VLM_SERVER_PORT} ✓")
            return
    except Exception:
        pass

    # Ensure model files exist (downloads from HF if missing)
    from vision.model.load import _ensure_downloaded

    _ensure_downloaded()

    print(f"[VLM] Starting llama-server on port {VLM_SERVER_PORT}...")
    _vlm_proc = subprocess.Popen(
        [
            VLM_SERVER_BINARY,
            "-m",
            VLM_MODEL_PATH,
            "--mmproj",
            VLM_MMPROJ_PATH,
            "-ngl",
            "99",
            "-c",
            "4096",
            "--port",
            str(VLM_SERVER_PORT),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("[VLM] Waiting for server to be ready (may take 30-60s on first run)...")
    for i in range(120):
        if _vlm_proc.poll() is not None:
            raise RuntimeError(
                f"[VLM] Server process died on startup (exit code {_vlm_proc.returncode}).\n"
                "Check that VLM_SERVER_BINARY and model paths are correct in config/vlm.py"
            )
        try:
            if requests.get(url, timeout=1).status_code == 200:
                print(f"[VLM] Server ready after {i}s ✓")
                return
        except Exception:
            pass
        if i > 0 and i % 15 == 0:
            print(f"[VLM] Still loading... ({i}s elapsed)")
        time.sleep(1)

    raise RuntimeError("[VLM] Server did not start within 120s. Check model paths.")


# ── Cleanup on exit ────────────────────────────────────────────────────────
import atexit


@atexit.register
def _cleanup():
    global _vlm_proc
    if _vlm_proc and _vlm_proc.poll() is None:
        print("[VLM] Shutting down server...")
        _vlm_proc.terminate()
        _vlm_proc = None


if __name__ == "__main__":
    main()
