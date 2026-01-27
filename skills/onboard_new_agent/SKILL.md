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
6. **Run any relevant skills**
7. **Write an onboarding snapshot** - Capture current goal, prior work, and next step in your `MEMORIES.md` file.

```
agent_assets/
└── <task_name>/      # task/project specific subdirectory
    ├── MEMORIES.md       # Knowledge base for ablation work
    └── code/         # Feature-specific temporary code
```

## Study the repo

- Look for high level summaries in README and docs files.
- Identify core code (the meat) that is relevant to the task.
- Seek to understand the workflow(s) being implemented (notebooks, CLI scripts, hardcoded scripts, job dispatching, etc.). Find entry points that lead to core code.
- Identify magic numbers, hardcoded paths, and parameters.

## Behavior expectations (align with repo rules)

- **Follow agentic instructions**.
- Maintain consistent behavior over long workflows.
- Writing and running lots of little code snippets is encouraged for development and debugging. Use the project-specific `code/` directory.
- Keep `MEMORIES.md` updated and high signal-to-noise.
- Place all generated artifacts (data, logs, etc.) related to temporary/agentic work in the task/project specific subdirectory of `agent_assets/`. Be liberal in storing artifacts.
- **Use and refresh skills** when relevant (e.g., `coding_style`, conversion tools), though avoid wasting context.
- Refrain from changing settings, installing packages, or otherwise modifying the environment unless explicitly asked.
- **Ask questions** when something is unclear or you can spot a potential problem down the line.

## Onboarding snapshot (write to MEMORIES.md)

Include the following, as they are relevant to the prompted task:
- Current goal and scope.
- What already exists and where (key files, scripts, commits, artifacts).
- Known issues and open questions.
- Next actionable step.

## skills

Skills are located in `.agent/skills/`. Each skill folder contains a `SKILL.md` with instructions. View the SKILL.md before using a skill.

| Skill | Purpose |
|-------|---------|
| `onboard_new_agent` | Onboard a new agent and summarize prior work |
| `refresh_context` | How to refresh context and understand a project quickly |
| `keeping_memories` | How to maintain and update MEMORIES.md files |
| `convert_scientific_notebook_to_script` | Convert Jupyter notebooks to standalone scripts |
| `convert_script_to_slurm_runs` | Create SLURM submission scripts from Python code |
| `coding_style` | Coding conventions for this project |
| `read-scientific-pdfs-mineru` | Read scientific PDFs using MinerU |
| `scientific_figure_export` | Export figures from scientific PDFs using MinerU |