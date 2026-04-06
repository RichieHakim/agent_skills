---
name: agent_guide
description: Rules and guidelines for agents
---

# Onboard or Refresh Context

## Workflow

1. Read `agent_environment.md` (bundled with this skill); run `keeping_memories` skill.
2. Find or create `agent_assets/<conversation_topic>/` with `MEMORIES.md`, `code/`, and `artifacts/`.
3. Read relevant prior agentic work:
   - Existing `agent_assets/**/MEMORIES.md` files that are relevant
   - Any other artifacts
4. Study the repo:
   - Top-level README/docs
   - Directory structure
   - Magic numbers, hardcoded paths, etc.
5. Load additional skills that are relevant
6. Determine the following and update `agent_assets/<conversation_topic>/MEMORIES.md` with:
   - Current goal and scope
   - What has been done
   - What exists and where (files, scripts, artifacts)
   - Known issues and open questions
   - Current status
   - Next actionable step

## Required Workspace Layout

All agent-only files must live under `agent_assets/<conversation_topic>/`:

```text
agent_assets/
└── <conversation_topic>/
    ├── MEMORIES.md
    ├── code/
    └── artifacts/
```

- `code/`: one-off scripts or utilities used only by the agent.
- `artifacts/`: logs, plots, manifests, README.md files, plan md files, LaTeX files/projects, paper pdfs, and test outputs. Stay organized and refactor with subdirectories as needed.

## `agent_assets/` is a symlink

`agent_assets/` is a symlink to permanent storage (`<agent_assets_meta_directory>`) so `$HOME` doesn't fill up. Resolve with `readlink agent_assets`.

- **If missing:** `mkdir -p <agent_assets_meta_directory> && ln -s <agent_assets_meta_directory> agent_assets`
- Don't delete, replace, or "fix" the symlink.
- Use `find -L` to traverse it
- Permissions/group are inherited from the target filesystem.
- Ensure `agent_assets/` is in `.gitignore`.

## If first-time onboarding

- Spend extra effort mapping out the repository.
- Create an initial `MEMORIES.md`.

## If refreshing context after a gap

- Use your knowledge of the codebase to ingest or reingest relevant files and code.
- Improve upon your map of the codebase and workflows.

## Behavior expectations (align with repo rules)

- **Follow agentic instructions**.
- Follow rules and guidelines over long workflows.
- Write and run little temporary test scripts often (placed in `agent_assets/code/`) for development and debugging.
- Keep `MEMORIES.md` updated and high signal-to-noise.
- **Proactively use and refresh skills**
- Do not change settings, install packages, or modify the environment unless explicitly asked.
- **Ask questions** if clarification could help.
- **Store artifacts** liberally.
  - Lightweight artifacts (i.e., notes, plots, logs) go in `agent_assets/`.
  - Large or permanent artifacts (i.e., `.npy`, models) go to `<temp_data_dir>` which is defined in `agent_environment.md`.