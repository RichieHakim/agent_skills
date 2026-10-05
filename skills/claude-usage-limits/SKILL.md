---
name: claude-usage-limits
description: Check the Claude account's usage limits (5-hour, and weekly if the plan has one). Use before dispatching agents and whenever a usage cut-off could lose work.
---

# Usage limits

All sessions and agents on the account share its limits. When one runs out, every affected agent stops with HTTP 429 until it resets.

```bash
python3 ~/.claude/skills/claude-usage-limits/check_usage.py        # % used and reset time for each limit
python3 ~/.claude/skills/claude-usage-limits/check_usage.py --raw  # full JSON
```

The script sends the local OAuth token only to `api.anthropic.com`; never print the token. The endpoint is undocumented.

To survive a cut-off event, you can instruct agents to write outputs under a temporary name and rename when done. Resume them by SendMessage after the reset, with a "check your state first" note.
