---
name: workspace-conventions
description: Workspace layout, artifact storage, and behavior rules shared by every agent (managers and subagents alike).
---

# Workspace conventions

## Workspace layout

All agent files live under `agent_assets/<topic>/` with subdirs: `MEMORIES.md`, `code/` (agent scripts), `artifacts/` (outputs, logs, plots, etc. — organize with subdirs).

## `agent_assets/` is a symlink

Symlinks to permanent storage (`<agent_assets_meta_directory>`) so `$HOME` doesn't fill up. Resolve with `readlink agent_assets`. Traverse with `find -L`. Don't delete or replace it. If missing: `mkdir -p <agent_assets_meta_directory> && ln -s <agent_assets_meta_directory> agent_assets`.

## Behavior

- Don't change settings, install packages, or modify the environment unless explicitly asked.
- Write and run small test scripts in `agent_assets/<topic>/code/`.
- Store lightweight artifacts in `artifacts/`; large files (`.npy`, models, checkpoints) go to `<temp_data_dir>` (see `references.md`).
