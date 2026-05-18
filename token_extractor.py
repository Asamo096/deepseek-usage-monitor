"""Optional browser token auto-extractor for platform.deepseek.com.

Uses Playwright to read localStorage from your Chrome browser profile.
Requires: pip install playwright && playwright install chromium

This is OPTIONAL — if Playwright is not installed or extraction fails,
the app falls back to the manual paste dialog.
"""

from __future__ import annotations
import os
import json

# Lazy import - only needed when auto-extract is attempted
_PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    _PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass

# Common Chrome user-data paths
_CHROME_PATHS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
    os.path.expandvars(r"%LOCALAPPDATA%\Chromium\User Data"),
    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data"),
]


def extract_token(auto_install: bool = False) -> str | None:
    """Try to extract the Bearer token from Chrome's localStorage.

    Returns the token string, or None if it couldn't be extracted.
    If auto_install is True and Playwright is missing, it will guide
    the user to install it.
    """
    if not _PLAYWRIGHT_AVAILABLE:
        if auto_install:
            print("Playwright not installed.")
            print("Install it with:  pip install playwright && playwright install chromium")
        return None

    user_data = _find_chrome_profile()
    if not user_data:
        return None

    try:
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=user_data,
                headless=True,
                channel="chrome",
                args=["--no-sandbox"],
            )
            page = ctx.new_page()
            page.goto("https://platform.deepseek.com/usage",
                      wait_until="domcontentloaded", timeout=15_000)

            token = page.evaluate(
                """() => {
                    try {
                        return JSON.parse(localStorage.getItem('userToken')).value;
                    } catch(e) {
                        return null;
                    }
                }"""
            )
            ctx.close()
            return token
    except Exception:
        return None


def _find_chrome_profile() -> str | None:
    """Find the first existing Chrome user data directory."""
    for base in _CHROME_PATHS:
        default_path = os.path.join(base, "Default")
        if os.path.isdir(default_path):
            return default_path
    return None
