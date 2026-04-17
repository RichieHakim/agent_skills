---
name: subagent-roles
description: Agent roles, models, and the dispatch pattern for delegating to subagents.
---

# Subagent Roles

## Dispatch pattern

Every dispatch prompt MUST include:
1. Role + skills: `Act as <role>. Load workspace-conventions, then: <skills>.`
2. Briefing: context or `MEMORIES.md` anchors. Give required specifics, but grant the subagent some freedom to use its judgement. Only micromanage less intelligent models.
3. Task: narrow scope, exact paths, deliverables, explicit non-goals ("do NOT touch X, Y").
4. Artifact target: explicit path for substantive findings, conventionally `agent_assets/<topic>/artifacts/reports/<HHMM>_<role>_<slug>.md`. The subagent can be as thorough as the task warrants there.
5. Response shape: concise triage — status, surprises, artifact paths; no prose.
6. Model: explicit (see `references.md`), don't just inherit.
7. Escalation: *"If uncertain, progress on clear parts, then stop with specific questions."*

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

Promote an ad-hoc dispatch into a role after 3+ repeats. Delete unused roles.
