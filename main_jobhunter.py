#!/usr/bin/env python3
# main_jobhunter.py

import sys
import time
import argparse

_vlm_proc = None


def main():
    parser = argparse.ArgumentParser(description="AI Job Hunter")
    parser.add_argument("--once",  action="store_true", help="Run one hunt cycle then exit")
    parser.add_argument("--site",  type=str, default=None, help="Hunt one specific site only")
    parser.add_argument("--stats", action="store_true", help="Show DB stats and exit")
    args = parser.parse_args()

    # ── Stats mode ─────────────────────────────────────────────────────────
    if args.stats:
        from jobhunter.storage import get_stats
        from jobhunter.config import CSV_PATH, DB_PATH
        stats = get_stats()
        print(f"\n{'='*40}")
        print(f"  Job Hunter Stats")
        print(f"{'='*40}")
        print(f"  Total jobs in DB : {stats['total']}")
        print(f"  Found today      : {stats['today']}")
        print(f"  CSV file         : {CSV_PATH}")
        print(f"  DB file          : {DB_PATH}")
        if stats["top_3"]:
            print(f"\n  Top matches:")
            for title, company, score in stats["top_3"]:
                print(f"    ★{score}  {title} @ {company}")
        print(f"{'='*40}\n")
        return

    # ── Start VLM server ────────────────────────────────────────────────────
    _start_vlm_server()

    # ── Load profile ────────────────────────────────────────────────────────
    from jobhunter.profile import PROFILE, SEARCH_QUERIES
    from jobhunter.logger import log

    log(f"Profile loaded: {PROFILE['name']}")
    log(f"Looking for: {', '.join(PROFILE['job_titles'][:2])}...")

    try:
        if args.site:
            site = args.site.lower()
            queries = SEARCH_QUERIES.get(site)
            if not queries:
                print(f"Unknown site '{site}'. Available: {list(SEARCH_QUERIES.keys())}")
                sys.exit(1)
            from jobhunter.lg_agent import hunt_site
            total = 0
            for q in queries:
                total += hunt_site(site, q, PROFILE)
            log(f"Done. {total} new jobs saved from {site}.")

        elif args.once:
            from jobhunter.lg_agent import run_full_hunt
            result = run_full_hunt(PROFILE, SEARCH_QUERIES)
            print(f"\nDone. {result['new_this_run']} new jobs saved.")

        else:
            from jobhunter.scheduler import start_scheduler
            try:
                start_scheduler()
            except KeyboardInterrupt:
                print("\n\nStopped by user.")

    finally:
        _stop_vlm_server()


def _start_vlm_server():
    global _vlm_proc
    import requests
    import subprocess
    from jobhunter.config import VLM_SERVER_PORT
    from config.vlm import VLM_SERVER_BINARY, VLM_MODEL_PATH, VLM_MMPROJ_PATH

    url = f"http://localhost:{VLM_SERVER_PORT}/health"
    try:
        if requests.get(url, timeout=2).status_code == 200:
            print(f"[VLM] Server already running on port {VLM_SERVER_PORT} ✓")
            return
    except Exception:
        pass

    print(f"[VLM] Starting llama-server on port {VLM_SERVER_PORT}...")
    _vlm_proc = subprocess.Popen(
        [VLM_SERVER_BINARY, "-m", VLM_MODEL_PATH, "--mmproj", VLM_MMPROJ_PATH,
         "-ngl", "99", "-c", "4096", "--port", str(VLM_SERVER_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("[VLM] Waiting for server to be ready...")
    for i in range(120):
        if _vlm_proc.poll() is not None:
            raise RuntimeError("[VLM] Server process died on startup.")
        try:
            if requests.get(url, timeout=1).status_code == 200:
                print(f"[VLM] Server ready after {i}s ✓")
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("[VLM] Server did not start within 120s.")


def _stop_vlm_server():
    global _vlm_proc
    if _vlm_proc:
        print("[VLM] Stopping llama-server...")
        _vlm_proc.terminate()
        _vlm_proc = None
        print("[VLM] Server stopped.")


if __name__ == "__main__":
    main()