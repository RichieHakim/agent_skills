---
name: figure-formatting
description: Guide for styling scientific figures with matplotlib. Use for any figure in this user's scientific work (reports, manuscripts, talks, analysis plots).
user-invocable: true
---

# Figure Formatting

Style for publication-ready matplotlib figures, matching the face-rhythm manuscript. Figures go to Illustrator, LaTeX manuscripts, and journals.

## Text

- **Font:** Arial. On Linux, render with `"Nimbus Sans"` (same metrics), then replace `Nimbus Sans` with `Arial` in the saved SVG text.
- **Size:** 8 pt minimum for all text, including ticks and keys. If text doesn't fit, abbreviate, rotate, remove, or redesign rather than shrink.
- **Panel titles:** ~10 pt, bold, lowercase except acronyms (PCA, EVR), centered over the panel. For a panel made of several axes, center the title over all of them, not over the first. Sub-panel titles: 8 pt, normal weight.
- **Axis labels:** the quantity in plain words, then its unit in parentheses: `frequency (Hz)`, `time (s)`. No code variable names, coined terms, or undefined abbreviations. Use `(a.u.)` only when the scale really is arbitrary; for a ratio, say what it is relative to: `firing rate (% of baseline)`.

## Panel labels

Label every panel of a multi-panel figure: A, B, C, 16 pt bold, near the top-left of the panel, aligned across rows and columns. For subdivisions, use B(i), B(ii) with the numeral at 8 pt normal weight, or just refer to left and right subpanels.

```python
fig.canvas.draw()
pos = ax.get_position()
fig.text(pos.x0 - 0.03, pos.y1 + 0.02, "A", fontsize=16, fontweight='bold', va='top', ha='left')
```

Offsets are figure fractions: 1 pt is `1/(72*H)` vertically and `1/(72*W)` horizontally for a figure of *W* × *H* inches.

## rcParams baseline

```python
from matplotlib import rcParams
rcParams.update({
    'font.family': 'Arial',
    'svg.fonttype': 'none', ## critical for editable text in Illustrator
    'pdf.fonttype': 42, ## TrueType — critical for editable text in PDF/Illustrator
    'font.size': 8,
    'axes.labelsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'axes.titlesize': 8,
    'axes.linewidth': 0.75,
    'xtick.major.width': 0.75,
    'ytick.major.width': 0.75,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'lines.linewidth': 1.0,
    'lines.markersize': 2.5,
    'legend.fontsize': 8,
    'legend.frameon': False,
})
```

## Plot elements

- **Axes:** left and bottom spines only, 0.75 pt. No gridlines without a reason. Bound axis ranges to meaningful limits (0 to 1, -100% to 100%).
- **Lines:** 1 pt, solid, no markers. To overlay two conditions, use color and drop the secondary trace to ~0.7 opacity rather than dashing it. Use transparency sparingly; it is hard to undo in Illustrator.
- **Statistics:** thin, transparent lines for each sample under a thick mean; shaded error band with no edge (`fill_between(..., alpha=0.3, linewidth=0)`). Choose SEM, STD, or CI deliberately.
- **Bars:** close together, with individual points overlaid (jittered, `s=12, alpha=0.7`). Error bars are a single 2 pt line with no cap: SEM or CI on summaries, STD on raw data.
- **Color:** perceptually uniform (`viridis`) or dichromatic colormaps. Compared panels share `vmin`/`vmax`; note it if they don't.
- **Images:** brighten slightly (`np.clip(img * 1.8, 0, 255)`). Crop with `set_xlim`/`set_ylim`, not slicing, to keep coordinates aligned with overlays. A border in a method's color can tie an image to that method.
- **Keys:** keep them off the data: below, beside, or in an empty region (`bbox_to_anchor`).

## Layout

- Minimize whitespace: At a minimum, use `gridspec` with `hspace`/`wspace` around 0.05–0.15. Try to remove the whitespace entirely.
- Size must find into a letter-sized manuscript: full text width, or narrow enough for text beside it. `figsize` doesn't change text size. Aim to make the figure small while maintaining easily readable text. Often individual figures are used as panels in a multi-panel figure.
- `set_box_aspect` fixes a panel's shape but overrides `hspace`; to close the gap, `fig.canvas.draw()` and then `ax.set_position([x0, y0, w, h])`.
- Give separable parts of a figure their own renderer function and output file, and compose them in a layout-only script.
- Break the grid with `fig.add_axes` when it helps, keeping styling and alignment consistent.

## Output

- Save PNG, SVG, and PDF with `dpi=600, bbox_inches='tight', pad_inches=0.1, transparent=False`. Use a lower dpi while the layout is moving. Ask the user about dpi for very large figures.
- Save in `artifacts/<potential intermediate dirs>/figures/YYYYMMDD_<figure>/` (see `workspace-conventions`).
- Inspect every render for overlaps, whitespace, and alignment, and fix in a loop or ask for help.
- SVG is the editable master. LaTeX uses the PDF; if it came from Illustrator, run `latex-pdf-preprocess` first. Trim excess margins with `pdfcrop --margins 2 in.pdf out.pdf`.
- For artists with more than ~1k points or SVGs over ~10 MB, ask the user whether to set `rasterized=True` on them.
- Compute the plotted quantities once into one container saved beside the figure, and plot only from it, so the figure regenerates from one small file. Use `.npz` for numbers, `zarr` or `h5` for large or mixed data, `richfile` for Python structures; not pickle.
- When available, use `bnpm.plotting_helpers.Figure_Saver` with `format_save=['svg', 'png']`, `svg_fontType='none'`, and the `savefig` kwargs above.
