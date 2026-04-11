---
name: workspace-conventions
description: Workspace layout, artifact storage, and behavior rules shared by every agent (managers and subagents alike).
---

# Workspace conventions

Where files go and how agents behave in this repo. Load alongside any role-specific skills — subagents load this instead of `manager`, which is scoped to the top-level agent.

## Required workspace layout

All agent-only files live under `agent_assets/<conversation_topic>/`:

```text
agent_assets/
└── <conversation_topic>/
    ├── MEMORIES.md
    ├── code/
    └── artifacts/
```

- `code/`: one-off scripts or utilities used only by the agent.
- `artifacts/`: logs, plots, manifests, README.md files, plan md files, LaTeX files/projects, paper pdfs, and test outputs. Stay organized and refactor with subdirectories as needed.

Subagents working under a parent inherit that parent's workspace unless the dispatch explicitly carves out a dedicated `agent_assets/<topic>/subagents/<sub_topic>/`.

## `agent_assets/` is a symlink

`agent_assets/` symlinks to permanent storage (`<agent_assets_meta_directory>`) so `$HOME` doesn't fill up. Resolve with `readlink agent_assets`. Traverse with `find -L`. Don't delete, replace, or "fix" it. If missing: `mkdir -p <agent_assets_meta_directory> && ln -s <agent_assets_meta_directory> agent_assets`.

## Behavior expectations

- **Follow instructions.** Rules and guidelines stick across long workflows.
- Write and run small temporary test scripts often (in `agent_assets/<topic>/code/`) for development and debugging.
- Do not change settings, install packages, or modify the environment unless explicitly asked. Ask before taking risky actions.
- Ask questions when clarification could help.
- Proactively use and refresh skills relevant to the task.
- Store artifacts liberally:
  - Lightweight (notes, plots, logs) → `agent_assets/<topic>/artifacts/`.
  - Large or permanent (`.npy`, models, checkpoints) → `<temp_data_dir>` (see `references.md` for the actual path).
