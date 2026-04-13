---
name: subagent-roles
description: Agent roles, models, and the dispatch pattern for delegating to subagents.
---

# Subagent Roles

## Dispatch pattern

Every dispatch prompt MUST include:

1. **Role and skills.** `Act as <role>. Load workspace-conventions, then: <skills>.`
2. **Briefing.** Inline context for small tasks; point at `## Section` anchors in `MEMORIES.md` for larger ones.
3. **Task.** Narrowly scoped. Exact paths, commands, deliverables.
4. **Response shape.** Verbosity cap and format. Default: *what you did / findings / artifacts / uncertainties*.
5. **Model.** Set explicitly (see `references.md`). Never inherit.
6. **Escalation rule** (verbatim): *"If you hit real uncertainty, make progress on the uncertainty-free parts, then stop and return with specific questions."*

Parallel dispatch: independent subtasks go in one message with multiple Agent calls.

## Roles

Every role loads `workspace-conventions` first. Subagents do **not** load `manager`. Add/remove skills as the task requires.

| Role | Skills | When |
|---|---|---|
| `computational-scientist` | `coding-style`, `script-opinions`, `figure-formatting` | AI/ML, data, stats, plots |
| `figure-maker` | `figure-formatting`, `latex-pdf-preprocess`, `illustrator` | Figures, Illustrator, PDF export |
| `script-refactorer` | `notebook-to-script`, `script-opinions`, `coding-style` | Notebooks/scripts → HPC-safe scripts |
| `job-dispatcher` | `job-dispatch`, `script-opinions`, `coding-style` | Compute job dispatching (local or SLURM), sweeps |
| `code-reviewer` | `coding-style`, `script-opinions`, `job-dispatch`, `simplify` | Review diffs for style/correctness |
| `literature-reviewer` | `read-pdf-mineru` | Extract and summarize scientific PDFs |
| `manuscript-writer` | `latex-manuscript`, `latex-pdf-preprocess`, `illustrator` | Draft/format manuscript sections, build PDFs |
| `sub-manager` | `manager`, `subagent-roles`, `keeping-memories` | Open-ended decomposition. Dedicated workspace. Depth < `<max_subagent_depth>`. Match parent model. |

Promote an ad-hoc dispatch into a role after 3+ repeats. Delete unused roles.
