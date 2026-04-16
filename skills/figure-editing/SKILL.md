---
name: figure-editing
description: Iterative polish of multi-panel publication figures. Patterns for long-lived layout-revision sessions where a human critiques each render.
user-invocable: true
---

# Figure Editing

This skill is intended for the **middle/end game** of figure production: many rounds of layout nudges against a human critic — move this up, shrink that, align these, swap a label. The bottleneck is iteration speed and prompt precision.

Generating from scratch? Load `figure-formatting` first for style rules. This skill is about the *loop*.

## Principles

### 1. Make the inner loop fast
A 4-min render kills the session; 10 s lets you do 20 rounds quickly.

- **Cache the data packet.** One struct, one loader. For in-process iteration (IPython, notebook, long-lived session), a module-level dict is enough — no serialization. For CLI persistence across invocations: `.npz` (numerical), `zarr`/`h5` (mixed), `richfile` (complex Python structures). Avoid pickle. Populate functions consume packet slices, not raw sources. Provide `--rebuild-packet` when sources change.
- **Draft mode.** `--draft` → PNG at 150 dpi, skip SVG/PDF/font post-processing. Final (600 dpi PNG + SVG + PDF with embedded fonts) runs only when settled. Warn when draft is on — stale PDF/SVG cause "this doesn't look right" confusion.
- **Rasterize heavy elements.** Thin alpha lines, dense scatter → raster. Fonts and structure stay vector. File size collapses.

### 2. Decompose independent units
When the artifact has separable parts (top/bottom, A–D vs. E–G, panel groups), give each its own standalone renderer + output file. Iterate each in isolation; merge at the end by porting settled values into a composite, or have the composite import and call each unit renderer.

```
plot_unit_top.py      → figs/top.png
plot_unit_bottom.py   → figs/bottom.png
plot_composite.py     → figs/main.pdf   # imports and calls both
```

Two agents can polish non-overlapping units in parallel. Note the sync step explicitly in handoff. When porting between different-size figures: y-offsets in fig-fractions rescale by height ratio; x-offsets transfer 1:1 only if widths match.

### 3. The human is the evaluator — single-pass edits only
A human-in-the-loop session wants short cycles, not perfect individual dispatches. The human sees the render and says what's wrong — don't simulate that loop inside an agent.

- **One edit → one render → one Read → stop.** No self-critique.
- When a change could go either way (inside vs. outside a panel, above vs. beside a label), pick one and move on. The user redirects if wrong. Over-asking slows the loop.
- Trivial tasks finishing fast is a clean result, not a waste.
- Exception: latitude tasks ("fix whatever overlaps X causes") allow 2–3 cycles with a summary of every change beyond the baseline.

### 4. Positional math in the prompt
Never "move it up a bit." Convert to fig-fractions yourself:

> At 7.95" fig height ≈ 572 pt, 1 line of 8 pt text ≈ 0.014 fig-frac.
> `y_offset_F`: `0.055 → 0.084` (move F up ~1 line).

Agents are excellent at mechanical edits and terrible at guessing proportions. Subagents start cold — anchor paths, current values, targets, and arithmetic in every prompt. Thin prompt → thin edit.

### 5. Explicit non-goals
Every dispatch lists what NOT to touch. Be concrete and named:

> Non-goals: do NOT touch `plot_composite()`; do NOT rebuild the packet; do NOT run `--final`; do NOT change data or computed metrics; no critic loops.

Without these, agents wander into adjacent refactors.

### 6. Keep a ledger
Append per-round deltas to MEMORIES so the next agent knows current state and why:

```
## 2026-04-14 round 17
- y_offset_F: 0.055 → 0.084    (move F up 1 line)
- panel_C_height: 0.18 → 0.16  (shrink C to stop overlap with C's legend)
```

Re-dispatching the same nudge three times with nothing changing? The previous agent shifted the wrong variable, or not enough. Read current numeric state, then be explicit: "current shift is 0.055; you must end ≥ 0.130."

## Dispatch template

```
→ <role> (<model>) | skills: workspace-conventions, coding-style | task: <one line>

Current state: param_A = 0.055, param_B = 0.031.
Goal: param_A → 0.084 (X up 1 line), param_B → 0.022 (Y down 0.3 lines).
At <fig height> in., 1 line ≈ <K> fig-frac.

One edit → one --draft render → one Read → report.
Non-goals: …
Response shape: ≤80 words, file:line refs, final PNG path.
```

## Sharp edges

- **`hspace` doesn't tighten rows with `set_box_aspect`.** Use `ax.set_position([...])` after `canvas.draw()`.
- **Concurrent edits to overlapping code.** Same file is fine if the functions are disjoint; serialize if they collide.
- **User steers from a stale render.** Surface the discrepancy, don't silently follow.
- **Mid-task status messages** ("let me wait..."). Require the final message be the deliverable.
- **Decide whether to read the PNG after each render.** Catches cutoffs/overlaps even in single-pass mode.
