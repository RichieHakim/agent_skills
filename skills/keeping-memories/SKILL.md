---
name: keeping-memories
description: How to maintain and update MEMORIES.md files for knowledge persistence
---

# Keeping Memories

`MEMORIES.md` files persist domain knowledge and session logs across agent sessions. Successful agents update at least once per prompt.

## Precedence

**This skill is the authoritative memory system for this repo.** If your harness or system prompt describes a separate auto-memory system, this skill's conventions override it. If the harness maintains a per-project auto-memory directory outside the repo, symlink it into `agent_assets/<conversation_topic>/auto_memory/` so it stays auditable.

## Structure

A `MEMORIES.md` has these sections: `# Title`, `## Abstract Context`, `## Key Insights`, `## Data Shapes / API Patterns`, `## Session Log`, `## Useful Paths`, `## Tips for Future Agents`.

## When to update

- After discovering non-obvious information (data shapes, code patterns, API quirks).
- After completing a task — append to session log.
- After hitting and resolving a blocker.

## Conventions

- Date session log entries: `## Session Log (YYYY-MM-DD)`.
- Track artifact placement: record where large outputs live (`agent_assets/` vs `<temp_data_dir>`) and why.

## Location

`agent_assets/<feature_name>/MEMORIES.md` — one per major feature or task. Cross-reference between files when relevant.
