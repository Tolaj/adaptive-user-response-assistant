# jobhunter/browser.py
# ─────────────────────────────────────────────────────────────────────────────
# Launches Playwright Chromium and injects real Chrome cookies from Keychain.
# Fixes: cookie field validation, browser stability, reconnection handling.
# ─────────────────────────────────────────────────────────────────────────────

import threading
import time
from jobhunter.config import SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT

COOKIE_DOMAINS = [
    "linkedin.com",
    "indeed.com",
    "naukri.com",
    "wellfound.com",
    "google.com",
]

_browser    = None   # keep browser alive at module level
_context    = None
_page       = None
_playwright = None
_lock       = threading.Lock()


def _clean_cookie(c) -> dict | None:
    """
    Convert a browser_cookie3 cookie into a valid Playwright cookie dict.
    Returns None if the cookie should be skipped.
    """
    import time as _time

    name  = getattr(c, "name",  None)
    value = getattr(c, "value", None)

    # Skip cookies with missing required fields
    if not name or value is None:
        return None

    # Domain: must start with dot for cross-subdomain cookies
    domain = getattr(c, "domain", "") or ""
    if not domain:
        return None
    if not domain.startswith("."):
        domain = "." + domain

    # Path
    path = getattr(c, "path", "/") or "/"

    # Expiry: must be a positive number in the future, or omitted
    expires = getattr(c, "expires", None)
    cookie = {
        "name":     name,
        "value":    str(value),
        "domain":   domain,
        "path":     path,
        "secure":   bool(getattr(c, "secure", False)),
        "httpOnly": False,
        "sameSite": "Lax",
    }

    # Only add expires if it's a valid future timestamp
    if expires and isinstance(expires, (int, float)) and expires > _time.time():
        cookie["expires"] = float(expires)

    return cookie


def _get_cookies() -> list[dict]:
    """Read Chrome cookies from macOS Keychain and clean them for Playwright."""
    try:
        import browser_cookie3
    except ImportError:
        raise RuntimeError("Run: pip install browser-cookie3")

    print("[Browser] Reading cookies from macOS Keychain...")
    all_cookies = []
    seen = set()

    for domain in COOKIE_DOMAINS:
        try:
            jar = browser_cookie3.chrome(domain_name=domain)
            for c in jar:
                cleaned = _clean_cookie(c)
                if cleaned is None:
                    continue
                # Deduplicate by name+domain
                key = (cleaned["name"], cleaned["domain"])
                if key in seen:
                    continue
                seen.add(key)
                all_cookies.append(cleaned)
        except Exception as e:
            print(f"[Browser] Skipped {domain}: {e}")

    print(f"[Browser] {len(all_cookies)} valid cookies loaded ✓")
    return all_cookies


def _create_browser_and_page():
    """Launch Playwright browser, inject cookies, return (browser, context, page)."""
    global _playwright

    from playwright.sync_api import sync_playwright

    if _playwright is None:
        _playwright = sync_playwright().start()

    cookies = _get_cookies()

    print("[Browser] Launching browser...")
    browser = _playwright.chromium.launch(
        headless=False,
        args=[
            f"--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
        ],
    )

    context = browser.new_context(
        viewport={"width": SCREENSHOT_WIDTH, "height": SCREENSHOT_HEIGHT},
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
    )

    # Inject cookies one by one — skip any that still fail
    injected, failed = 0, 0
    for cookie in cookies:
        try:
            context.add_cookies([cookie])
            injected += 1
        except Exception:
            failed += 1

    print(f"[Browser] Injected {injected} cookies ({failed} skipped) ✓")

    page = context.new_page()

    # Keep browser alive — attach close handler to detect crashes
    def _on_close():
        print("[Browser] Browser window was closed.")

    browser.on("disconnected", _on_close)

    return browser, context, page


def get_browser():
    """Get a ready page. Auto-recovers if browser was closed."""
    global _browser, _context, _page, _playwright

    # Fast path — check if existing page is alive
    if _page is not None:
        try:
            _ = _page.url   # lightweight liveness check (cheaper than title())
            return _page
        except Exception:
            print("[Browser] Page lost — relaunching browser...")
            _page    = None
            _context = None
            _browser = None

    with _lock:
        if _page is not None:
            return _page

        _browser, _context, _page = _create_browser_and_page()
        print(f"[Browser] Ready ✓ — logged in as swapnilhgf@gmail.com")

    return _page


def release_browser():
    """Close the job hunter browser. Your real Chrome is untouched."""
    global _browser, _context, _page, _playwright

    with _lock:
        _page = None
        _context = None

        if _browser:
            try:
                _browser.close()
            except Exception:
                pass
            _browser = None

        if _playwright:
            try:
                _playwright.stop()
            except Exception:
                pass
            _playwright = None

        print("[Browser] Closed. Your Chrome is untouched.")


def navigate(url: str) -> None:
    from jobhunter.config import PAGE_LOAD_WAIT_MS
    page = get_browser()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(PAGE_LOAD_WAIT_MS)
    except Exception as e:
        print(f"[Browser] Navigation error: {e} — retrying...")
        time.sleep(2)
        page = get_browser()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(PAGE_LOAD_WAIT_MS)


def current_url() -> str:
    try:
        return get_browser().url
    except Exception:
        return ""