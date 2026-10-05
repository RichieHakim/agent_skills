#!/usr/bin/env python3
"""
Print the account's usage limits (5-hour, and weekly where the plan has one) from Anthropic's OAuth usage endpoint.

Reads the Claude Code OAuth access token from ~/.claude/.credentials.json and never prints it.
Stdlib only, so it runs under any python3.
"""

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

URL_USAGE = "https://api.anthropic.com/api/oauth/usage"


def to_local(timestamp):
    """ISO-8601 timestamp -> local time; returns the input unchanged on python < 3.7 or bad input."""
    try:
        return datetime.fromisoformat(timestamp).astimezone().strftime("%a %Y-%m-%d %H:%M %Z")
    except (AttributeError, TypeError, ValueError):
        return timestamp


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path_credentials", default=str(Path.home() / ".claude" / ".credentials.json"))
    parser.add_argument("--raw", action="store_true", help="print the full JSON response")
    args = parser.parse_args()

    oauth = json.loads(Path(args.path_credentials).read_text())["claudeAiOauth"]
    seconds_left = oauth["expiresAt"] / 1000 - time.time()
    if seconds_left <= 0:
        raise SystemExit(f"access token expired {-seconds_left / 60:.0f} min ago; any Claude Code request refreshes it")

    request = urllib.request.Request(
        URL_USAGE,
        headers={
            "Authorization": f"Bearer {oauth['accessToken']}",
            "anthropic-beta": "oauth-2025-04-20",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            usage = json.loads(response.read())
    except urllib.error.HTTPError as error:
        raise SystemExit(f"HTTP {error.code}: {error.read()[:300]!r}")

    if args.raw:
        print(json.dumps(usage, indent=2))
        return
    print(time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    # Older plans report windows as top-level keys (five_hour, seven_day, ...); newer ones list them under "limits".
    for name, window in usage.items():
        if isinstance(window, dict) and window.get("utilization") is not None:
            print(f"{name:24s} {window['utilization']!s:>6}%  resets {to_local(window.get('resets_at'))}")
    for limit in usage.get("limits") or []:
        model = ((limit.get("scope") or {}).get("model") or {}).get("display_name")
        name = f"{limit.get('group') or limit.get('kind')}" + (f" ({model})" if model else "")
        inactive = "" if limit.get("is_active", True) else "  (inactive)"
        print(f"{name:24s} {limit.get('percent')!s:>6}%  resets {to_local(limit.get('resets_at'))}{inactive}")


if __name__ == "__main__":
    main()
