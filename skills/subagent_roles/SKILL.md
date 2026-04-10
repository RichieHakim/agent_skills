---
name: subagent_roles
description: Subagent roles and the dispatch patterns.
---

# Subagent Roles

A **switchboard**: pick a role, dispatch a subagent with it. Roles are *suggestive* — they bundle default skills, but subagents may load others if needed.

## Dispatch pattern

Every dispatch prompt MUST include:

1. **Role.** `Act as <role_name>.`
2. **Skills.** `Load agent_guide, then this role's skills: <list>.`
3. **Briefing.** Inline context, or pointers to specific `## Section` anchors in the manager's `MEMORIES.md` (flag it as living/actively updated).
4. **Task.** Scoped small. Exact paths, commands, deliverables.
5. **Response shape.** Verbosity cap and format. Default: *<200 words; what you did / findings / artifacts / uncertainties*.
6. **Escalation rule** (verbatim): *"If you hit real uncertainty, make progress on the uncertainty-free parts, organize what you have, then stop and return with specific questions rather than guessing."*
7. **Workspace.** Shared (`agent_assets/<topic>/`) or dedicated (`.../subagents/<name>/`).

**Parallel dispatch.** Independent subtasks require multiple Agent calls in a single message.

## Roles

`agent_guide` is always loaded alongside the skills below.

### `data_analyst`
- **Skills:** `xlsx`, `figure_formatting`, `coding_style`
- **When:** analyze spreadsheets, compute stats, produce plots.

### `script_refactorer`
- **Skills:** `convert_scientific_notebook_to_script`, `coding_style`
- **When:** turn notebooks into HPC/batch-safe scripts.

### `slurm_dispatcher`
- **Skills:** `convert_script_to_slurm_runs`, `coding_style`
- **When:** package scripts for SLURM, launch array jobs (use `%15`).

### `literature_reviewer`
- **Skills:** `read_pdf_mineru`
- **When:** extract and summarize scientific PDFs.

### `manuscript_writer`
- **Skills:** `latex_manuscript`, `latex_pdf_preprocess`, `illustrator`, `figure_formatting`
- **When:** draft/format manuscript sections, prepare figures, build PDFs.

### `code_reviewer`
- **Skills:** `coding_style`, `simplify`
- **When:** review diffs for style, complexity, correctness.

### `sub_manager`
- **Skills:** `manager`, `subagent_roles`, `keeping_memories`
- **When:** open-ended decomposition that would flood the parent's context.
- **Workspace:** `agent_assets/<topic>/subagents/<sub_topic>/` with its own `MEMORIES.md`, `code/`, `artifacts/`.
- **Hierarchy:** allowed only if parent depth < `<max_subagent_depth>` (see `manager`).

## Adding new roles

New `### <role_name>` section with **Skills** and **When**. Add when a pattern repeats; remove when unused.
