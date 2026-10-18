---
name: workspace-conventions
description: Workspace layout, artifact storage, and behavior rules shared by every agent (managers and subagents alike).
---

# Workspace conventions

## Layout

All agent files live in `agent_assets/`, one folder per topic:

```text
agent_assets/
├── README.md                          # optional index of topics
├── auto-memory/                       # see keeping-memories
└── YYYYMMDD_<slug>/                   # one topic
    ├── MEMORIES.md
    ├── code/YYYYMMDD_<task>/          # one task's scripts
    └── artifacts/
        ├── reports/YYYYMMDD-HHMM_<role>_<slug>.md
        ├── figures/YYYYMMDD_<figure>/ # data, renders, drafts, critic logs
        ├── work/YYYYMMDD_<task>/      # outputs and logs of code/YYYYMMDD_<task>/
        └── files/YYYYMMDD_<slug>/     # files from the user, downloaded papers
```

- **Only what the tree shows** goes at these levels. Plans, briefs, and handoffs are reports. A report made of several files, like LaTeX, gets a dated folder in `reports/`. Inside a dated folder, name things freely.
- **Date every folder you add** with the day it was created. Reports add the time. Get both from `date +%Y%m%d-%H%M`, never from memory. A slug is two to four lowercase words joined by hyphens; on a same-day clash, append `_02`.
- **A task's code and outputs share one name:** `code/20261017_push-directions/` writes to `artifacts/work/20261017_push-directions/`.
- **Drafts and backups go inside the folder** of the thing they belong to, not beside it.
- **File it right the first time.** Notes and scripts cite absolute paths, so moves break them. Don't rename, move, or delete existing folders unless the user asks.

## Topics

Before creating a topic, run `ls -1 agent_assets/`. If one already covers the work, use it; don't start one per session, subagent, or attempt. When the work turns to a new question or deliverable, start a new topic and link to it from the old `MEMORIES.md`.

## `agent_assets/` is a symlink

Symlinks to permanent storage (`<agent_assets_meta_directory>`) so `$HOME` doesn't fill up. Resolve with `readlink agent_assets`. Traverse with `find -L`. Don't delete or replace it. If missing: `mkdir -p <agent_assets_meta_directory> && ln -s <agent_assets_meta_directory> agent_assets`.

## Behavior

- Don't change settings, install packages, or modify the environment unless explicitly asked.
- Large files (`.npy`, models, checkpoints) go to `<temp_data_dir>` (see `references.md`), not `artifacts/`.
