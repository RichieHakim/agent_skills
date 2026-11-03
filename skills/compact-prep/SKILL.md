---
name: c
description: Prepare for /compact so that the agent after compaction starts with a clean context and loses nothing that matters. Invoked as /compact-prep or its short form /c. Use when the user types either, says that you are bloated, or asks you to prepare for compaction.
argument-hint: "[p]"
---

# Compact prep

The user will run `/compact` next. Save what matters to files, so that the summary only needs to point to them. Don't start new work.

If the user added `p`, as in `/c p`, they want you to proceed after compaction: take the next step without checking in, unless their next message says otherwise.

## Before compaction

1. Make `artifacts/reports/<YYYYMMDD-HHMM>_manager_compact-handoff/` and copy into it each MEMORIES.md that you will change.
2. Update each active topic's MEMORIES.md: add what you learned, merge duplicates, and delete inaccuracies and things that are certainly no longer relevant. Compress the text to an absolute minimum. However, do not throw away the overall process of what has happened from beginning to end, and keep knowledge that could be useful later.
3. Write `handoff.md` in that folder, under 40 lines: the goal and next step, the user's rules and corrections in their words, approvals marked used or expired, running work, whether to proceed (`p`), and the paths of each MEMORIES.md and the transcript (`~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl`). Link it from each MEMORIES.md.
4. Reply in two lines: where the handoff is, and the line to paste: `/compact Keep this short. Resume from <handoff path>.`, adding `Then proceed with the next step.` for `p`.
5. If the length of the MEMORIES.md or handoff is more than ~10k tokens, advise the user.

## After compaction

Reload your skills and read the handoff. If it says to proceed, take the next step.
