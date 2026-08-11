---
name: workspace-conventions
description: Workspace layout, artifact storage, and behavior rules shared by every agent (managers and subagents alike).
---

# Workspace conventions

## Workspace layout

All agent files live under `agent_assets/<topic>/` with subdirs: `MEMORIES.md`, `code/` (agent scripts), `artifacts/` (outputs, logs, plots, etc. — organize with subdirs).

## Naming `<topic>` directories

Name the topic directory `YYYYMMDD_<slug>`, where the date is the day the work started
and the slug is two to four lowercase words joined by hyphens. Example:
`agent_assets/20260811_janelia-talk-description/`.

If two topics start on the same day, append `_NN` starting at `_02`:
`20260811_janelia-talk-description_02`.

Before creating a directory, run `ls -1 agent_assets/` and read the names. If a
directory already covers this work, use it. Do not create a new one per session, per
subagent, or per attempt. The date records when the work started, not when you looked
at it.

Do not rename or delete an existing topic directory unless the user asks.

## `agent_assets/` is a symlink

Symlinks to permanent storage (`<agent_assets_meta_directory>`) so `$HOME` doesn't fill up. Resolve with `readlink agent_assets`. Traverse with `find -L`. Don't delete or replace it. If missing: `mkdir -p <agent_assets_meta_directory> && ln -s <agent_assets_meta_directory> agent_assets`.

## Behavior

- Don't change settings, install packages, or modify the environment unless explicitly asked.
- Write and run small test scripts in `agent_assets/<topic>/code/`.
- Store lightweight artifacts in `artifacts/`; large files (`.npy`, models, checkpoints) go to `<temp_data_dir>` (see `references.md`).
