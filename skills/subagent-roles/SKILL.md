---
name: subagent-roles
description: Subagent roles and the dispatch pattern.
---

# Subagent Roles

A **switchboard**: pick a role, dispatch a subagent with it. Roles are *suggestive* — they bundle default skills, but subagents may load others if needed.

## Dispatch pattern

Every dispatch prompt MUST include:

1. **Role.** `Act as <role_name>.`
2. **Skills.** `Load agent-guide, then this role's skills: <list>.`
3. **Briefing.** Inline context, or pointers to specific `## Section` anchors in the manager's `MEMORIES.md` (flag it as living/actively updated).
4. **Task.** Scoped small. Exact paths, commands, deliverables.
5. **Response shape.** Verbosity cap and format. Default: *<200 words; what you did / findings / artifacts / uncertainties*.
6. **Escalation rule** (verbatim): *"If you hit real uncertainty, make progress on the uncertainty-free parts, organize what you have, then stop and return with specific questions rather than guessing."*
7. **Workspace.** Shared (`agent_assets/<topic>/`) or dedicated (`.../subagents/<name>/`).

**Parallel dispatch.** Independent subtasks require multiple Agent calls in a single message.

## Roles

`agent-guide` is always loaded alongside the skills below.

### `data-analyst`
- **Skills:** `xlsx`, `figure-formatting`, `coding-style`
- **When:** analyze spreadsheets, compute stats, produce plots.

### `script-refactorer`
- **Skills:** `notebook-to-script`, `script-opinions`, `coding-style`
- **When:** turn notebooks into HPC/batch-safe scripts.

### `slurm-dispatcher`
- **Skills:** `slurm-dispatch`, `script-opinions`, `coding-style`
- **When:** package scripts for SLURM, launch array jobs (use `%15`).

### `literature-reviewer`
- **Skills:** `read-pdf-mineru`
- **When:** extract and summarize scientific PDFs.

### `manuscript-writer`
- **Skills:** `latex-manuscript`, `latex-pdf-preprocess`, `illustrator`, `figure-formatting`
- **When:** draft/format manuscript sections, prepare figures, build PDFs.

### `code-reviewer`
- **Skills:** `coding-style`, `simplify`
- **When:** review diffs for style, complexity, correctness.

### `sub-manager`
- **Skills:** `manager`, `subagent-roles`, `keeping-memories`
- **When:** open-ended decomposition that would flood the parent's context.
- **Workspace:** `agent_assets/<topic>/subagents/<sub_topic>/` with its own `MEMORIES.md`, `code/`, `artifacts/`.
- **Hierarchy:** allowed only if parent depth < `<max_subagent_depth>` (see `manager`).

## Adding new roles

New `### <role-name>` section with **Skills** and **When**. Add when a pattern repeats; remove when unused.
