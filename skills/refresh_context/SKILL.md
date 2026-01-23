---
name: refresh_context
description: How to refresh context and understand a project quickly
---

# Refreshing Context

When starting work on an existing project or after a long gap, quickly orient yourself by reading key files in order.

## Steps

1. **Read top-level `AGENTS.md`** - Contains project-specific parameters and instructions

2. **Find or make an `agent_assets/<conversation_topic>` directory** - This is your personal knowledge store. Find or make the following within this directory:
   - A project-specific `MEMORIES.md` files. If this exists, read it carefully.
   - A `code/` subdirectory for one-off/temporary utility scripts called only by the agent (these are not made part of the repo)
   - An `artifacts/` subdirectory for agent-only logs or test outputs.

3. **Look through available skills**
   - Read/ingest the `keeping_memories` skill and begin logging important information to the appropriate `MEMORIES.md` file
   - Decide which other skills are relevant to study and possibly read them

4. **Check conversation summary** (if available):
   - Review any conversation summaries
   - Note the current status of the task/goal
   - Identify blocking issues and next steps