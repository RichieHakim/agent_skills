---
name: subagent-roles
description: Agent roles, models, and the dispatch pattern for delegating to subagents.
---

# Subagent Roles

A role bundles a default skill set, model, and workspace convention. The manager picks a role, fills in the dispatch pattern, and calls the Agent tool. Subagents may load extra skills if the task needs them.

## Dispatch pattern

Every dispatch prompt MUST include:

1. **Role and skills.** `Act as <role>. Load workspace-conventions, then: <skills>.`
2. **Briefing.** Inline context for small self-contained tasks; otherwise point at specific `## Section` anchors in `MEMORIES.md` and flag the file as actively maintained, not frozen.
3. **Task.** Narrowly scoped. Exact paths, commands, deliverables. Name the workspace directory if it differs from the parent's default.
4. **Response shape.** Verbosity cap and format. Default: *what you did / findings / artifacts / uncertainties*.
5. **Model.** Set the Agent tool's `model` parameter explicitly — never inherit. See "Model selection" below.
6. **Escalation rule** (verbatim): *"If you hit real uncertainty, make progress on the uncertainty-free parts, organize what you have, then stop and return with specific questions rather than guessing."*

**Parallel dispatch.** Independent subtasks go in a single message with multiple Agent calls.

## Workspaces

Subagents inherit the parent's workspace (`agent_assets/<topic>/`) unless the role or task says otherwise. Only carve out a dedicated `agent_assets/<topic>/subagents/<sub_topic>/` when the work is self-contained enough that a fresh reader should audit it in isolation. `sub-manager` always gets its own.

## Model selection

Select an appropriate model given the task requirements. Tasks that are challenging or require a high degree of trust should use more capable models. Model names are in `references.md`. Pass the model name explicitly when dispatching.

## Roles

Every role loads `workspace-conventions` first, in addition to the suggested list of skills (add/remove/edit this list as appropriate for the task). Subagents do **not** load `manager` — that's scoped to the top-level agent running the conversation.

| Role | Skills available | When |
|---|---|---|
| `computational-scientist` | `coding-style`, `script-opinions`, `figure-formatting` | AI/ML, data, stats, plots. |
| `figure-maker` | `figure-formatting`, `latex-pdf-preprocess`, `illustrator` | Making and editing figures, controlling adobe illustrator, exporting figure pdfs. |
| `script-refactorer` | `notebook-to-script`, `script-opinions`, `coding-style` | Turn notebooks or one-off scripts into HPC/batch-safe scripts. |
| `slurm-dispatcher` | `slurm-dispatch`, `script-opinions`, `coding-style` | Package scripts for SLURM, launch arrays or sweeps. |
| `code-reviewer` | `coding-style`, `script-opinions`, `slurm-dispatch`, `simplify` | Review diffs for style, complexity, correctness. |
| `literature-reviewer` | `read-pdf-mineru` | Extract and summarize scientific PDFs. |
| `manuscript-writer` | `latex-manuscript`, `latex-pdf-preprocess`, `illustrator` | Draft or format manuscript sections, prepare figures, build PDFs. |
| `sub-manager` | `manager`, `subagent-roles`, `keeping-memories` | Open-ended decomposition that would flood the parent's context. Dedicated workspace required. Only allowed if parent depth < `<max_subagent_depth>` (see `manager`). Match parent's model. |

## Adding or removing roles

Promote an ad-hoc dispatch into a role only after the same skill+model combo has repeated three or more times. Delete roles that go unused — a stale table is worse than a short one. Don't list a skill that doesn't exist in this repo or in the CLI-bundled set.
