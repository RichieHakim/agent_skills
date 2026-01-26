---
name: onboard_new_agent
description: Onboard a new agent to a repo using existing artifacts, refresh_context, and prior work signals
---

# Onboard a New Agent

Goal: bring a new agent up to speed on expected behavior and existing work without introducing new repo structures.

## Quick Start

1. **Run the `refresh_context` skill**
2. **Run the `keeping_memories` skill**
3. Open and read through any existing and relevant files within `agent_assets/`, especially `MEMORIES.md` files.
4. Create new `agent_assets/<task_name>/` directory and populate with `code/`, `artifacts/`, and `MEMORIES.md`.
5. **Study the repo**
6. **Write an onboarding snapshot** - Capture current goal, prior work, and next step in your `MEMORIES.md` file.

## Study the repo

- Look for high level summaries in README and docs files.
- Identify core code (the meat) that is relevant to the task.
- Seek to understand the workflow(s) being implemented (notebooks, CLI scripts, hardcoded scripts, job dispatching, etc.). Find entry points that lead to core code.
- Identify magic numbers, hardcoded paths, and parameters.

## Behavior expectations (align with repo rules)

- **Follow agentic instructions**.
- Maintain consistent behavior over long workflows.
- Keep `MEMORIES.md` updated and high signal-to-noise.
- **Use and refresh skills** when relevant (e.g., `coding_style`, conversion tools), though avoid wasting context.
- Refrain from changing settings, installing packages, or otherwise modifying the environment unless explicitly asked.
- **Ask questions** when something is unclear or you can spot a potential problem down the line.

## Onboarding snapshot (write to MEMORIES.md)

Include the following, as they are relevant to the prompted task:
- Current goal and scope.
- What already exists and where (key files, scripts, commits, artifacts).
- Known issues and open questions.
- Next actionable step.
