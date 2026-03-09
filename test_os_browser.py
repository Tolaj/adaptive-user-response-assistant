#!/usr/bin/env python3
# test_os_browser.py
# ─────────────────────────────────────────────────────────────────────────────
# Smoke test for the OS-level browser automation.
# Run this FIRST before plugging into the full job hunter.
#
# What it does:
#   1. Takes a screenshot — verifies screencapture works
#   2. Launches Chrome
#   3. Uses VLM to find and click the swapnilhgf@gmail.com profile
#   4. Navigates to google.com
#   5. Searches for "python developer jobs"
#
# Usage:
#   python test_os_browser.py
#
# Requirements:
#   pip install pyautogui pyperclip Pillow
#   VLM server must be running on port 8081 (start your normal app first)
# ─────────────────────────────────────────────────────────────────────────────

import sys
import time

TARGET_EMAIL = "swapnilhgf@gmail.com"
START_URL    = "https://www.google.com"


def main():
    print("\n" + "="*55)
    print("  OS Browser Automation — Smoke Test")
    print("="*55 + "\n")

    # ── Step 0: Verify VLM server is running ──────────────────────────────
    _check_vlm()

    # ── Step 1: Take a test screenshot ────────────────────────────────────
    print("[1/5] Taking test screenshot...")
    from jobhunter.os_snap import snap_screen_b64, get_screen_size
    b64 = snap_screen_b64()
    print(f"  ✓ Screenshot OK — {len(b64)} chars, screen size: {get_screen_size()}")

    # ── Step 2: Launch Chrome ─────────────────────────────────────────────
    print("\n[2/5] Launching Chrome...")
    from jobhunter.os_browser import launch_chrome
    launch_chrome()
    print("  ✓ Chrome launch command sent.")

    # Give Chrome 3 seconds to fully open
    print("  Waiting 3s for Chrome to appear...")
    time.sleep(3)

    # ── Step 3: Select profile ────────────────────────────────────────────
    print(f"\n[3/5] Selecting Chrome profile: {TARGET_EMAIL}")
    print("  (VLM will look at your screen and click the right profile)")

    from jobhunter.os_actions import decide_action, execute_action

    profile_goal = (
        f"I need to select the Chrome profile for '{TARGET_EMAIL}'. "
        f"If you see a 'Who's using Chrome?' profile picker screen, "
        f"click on the avatar/name matching '{TARGET_EMAIL}'. "
        f"If Chrome is already showing a browser window (no profile picker), "
        f"respond with action=already_open. "
        f"Click the correct profile or say already_open."
    )

    for attempt in range(5):
        print(f"  Attempt {attempt+1}/5: asking VLM what to do...")
        action = decide_action(profile_goal)
        action_type = action.get("action", "unknown")
        print(f"  VLM says: {action_type} — {action.get('reason', '')}")

        if action_type == "already_open":
            print("  ✓ Chrome already on main window.")
            break
        elif action_type == "click":
            execute_action(action)
            time.sleep(2.5)
            print("  ✓ Clicked profile.")
            break
        else:
            print(f"  Unexpected action '{action_type}', waiting and retrying...")
            time.sleep(2)

    # ── Step 4: Navigate to Google ────────────────────────────────────────
    print(f"\n[4/5] Navigating to {START_URL}...")
    from jobhunter.os_browser import navigate
    navigate(START_URL, wait_sec=3)
    print(f"  ✓ Navigated to {START_URL}")

    # ── Step 5: Type a search query ───────────────────────────────────────
    print("\n[5/5] Testing search — typing into Google search box...")
    print("  (VLM will find the search box and click it)")

    search_goal = (
        "I see Google's homepage. "
        "Click on the search box (the main text input in the center of the page). "
        "Respond with action=click and the x,y coordinates of the search input."
    )

    for attempt in range(3):
        action = decide_action(search_goal)
        if action.get("action") == "click":
            execute_action(action)
            time.sleep(0.5)
            # Now type the search query
            from jobhunter.os_browser import type_text, press_enter
            type_text("python developer jobs remote")
            time.sleep(0.3)
            press_enter()
            time.sleep(2)
            print("  ✓ Search submitted!")
            break
        time.sleep(1.5)

    # ── Done ──────────────────────────────────────────────────────────────
    print("\n" + "="*55)
    print("  ✓ All steps complete!")
    print("  Check your screen — Chrome should show Google search results.")
    print("="*55 + "\n")
    print("If everything looks good, the OS automation is working.")
    print("You can now run: python main_jobhunter.py --once\n")


def _check_vlm():
    import requests
    from jobhunter.config import VLM_SERVER_PORT

    url = f"http://localhost:{VLM_SERVER_PORT}/health"
    print(f"[0/5] Checking VLM server on port {VLM_SERVER_PORT}...")
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            print(f"  ✓ VLM server running.\n")
            return
    except Exception:
        pass

    print(f"\n  ✗ VLM server NOT running on port {VLM_SERVER_PORT}.")
    print("  Start it first:")
    print(f"    llama-server -m <model.gguf> --mmproj <mmproj.gguf> -ngl 99 -c 2048 --port {VLM_SERVER_PORT}")
    print("  Or set MODE='vision_text' in config/features.py and run main.py\n")
    sys.exit(1)


if __name__ == "__main__":
    main()