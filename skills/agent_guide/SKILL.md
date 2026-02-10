---
name: agent_guide
description: Rules and guidelines for agents
---

# Onboard or Refresh Context

## Workflow

1. Read top-level `AGENTS.md` and extract hard constraints.
2. Find or create `agent_assets/<conversation_topic>/` with `MEMORIES.md`, `code/`, and `artifacts/`.
3. Read relevant prior work:
   - Existing `agent_assets/**/MEMORIES.md` files relevant to the current goal.
   - Any pointers/manifests for prior outputs.
4. Study the repo:
   - Top-level README/docs.
   - Core entry points and scripts/modules tied to the task.
   - Magic numbers, hardcoded paths, and fragile assumptions.
5. Load supporting skills:
   - Discover skills in `.agent/skills` and `.agent/repo_skills` (if present).
   - Run the `keeping_memories` skill.
   - Read additional skills that are relevant to the task.
6. Check conversation summary (if available):
   - Current status.
   - Blocking issues.
   - Next actionable step.
7. Update `agent_assets/<conversation_topic>/MEMORIES.md` with:
   - Current goal and scope.
   - What exists and where (files, scripts, artifacts).
   - Known issues and open questions.
   - Next actionable step.

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
- `artifacts/`: temporary logs, manifests, and test outputs.

## If first-time onboarding

- Spend extra effort mapping out the repository structure and workflows.
- Create an initial baseline snapshot of state and goals in `MEMORIES.md`.

## If refreshing context after a gap

- Use your knowledge of the codebase to ingest relevant files and code.
- Improve upon your map of the codebase and workflows.

## Behavior expectations (align with repo rules)

- **Follow agentic instructions**.
- Follow rules over long workflows.
- Write and run little temporary test scripts often (placed in `agent_assets/code/`) for development and debugging.
- Keep `MEMORIES.md` updated and high signal-to-noise.
- **Use and refresh skills** (e.g., `coding_style`, conversion tools). Keep track of which skills are available to you and use them when relevant.
- Refrain from changing settings, installing packages, or otherwise modifying the environment unless explicitly asked.
- **Ask questions** when something is unclear or you can spot a potential problem down the line.
- **Store artifacts** liberally.
  - Keep lightweight and scannable artifacts in `agent_assets/` (notes, manifests, small logs, plots, tables, tiny checkpoints).
  - Route larger artifacts (for example large `.pkl/.npy/.npz`, model checkpoints, full run dumps, cache directories) to `<temp_data_dir>` when defined in `AGENTS.md`.
  - Leave a pointer/manifest in `agent_assets/<conversation_topic>/artifacts/` for anything moved out.
