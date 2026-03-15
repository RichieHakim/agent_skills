---
name: figure-formatting
description: Guide for styling scientific figures with matplotlib.
user-invokable: true
---

# Figure Formatting

Style guide for generating publication-ready scientific figures with matplotlib. These conventions match the visual language of the face-rhythm manuscript and should be applied to all new figures.

## Typography

- **Font**: Arial (or Helvetica as fallback).
- **Minimum size**: 8 pt for all text including tick labels, axis labels, legends, and annotations.
- **Titles and labels**: ~10 pt and lowercase except for acronyms (e.g., PCA, EVR, BMI, etc.). This includes axis labels, column headers, and figure titles.
- **Units**: parenthesized after label, e.g., `frequency (Hz)`, `time (s)`, `(a.u.)`.

## rcParams baseline

Adjust the following `rcParams` settings as needed to ensure consistent typography and styling.

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

## Axes and spines

- **Remove top and right spines** on line/scatter plots. Only keep left and bottom.
- Spine and tick width: 0.75 pt.

## Lines

- Default line width: 1 pt
- Use solid lines. Avoid dashes unless absolutely necessary for accessibility on a single overlaid axis.
- When overlaying two methods/conditions, try to differentiate with color and reduce opacity of the secondary trace (~0.7) rather than using dashes.

## Transparency and opacity

- Use alpha/transparency **sparingly**. It is difficult to increase opacity post-hoc in Illustrator.

## Colormaps and normalization

- Use **perceptually uniform** colormaps (e.g., `viridis`) unless there is a strong reason not to. Dichromatic colormaps are also good.
- For comparison across panels, use **shared normalization** (same `vmin`/`vmax`). Document if per-panel normalization is used.

## Images and spatial maps

- For scientific images, it is recommended to brighten and oversaturate slightly.
- It is wise to crop images using `set_xlim` / `set_ylim` rather than array slicing (preserves coordinate alignment with scatter data).
- When images represent different methods/conditions, adding a colored border (spine stroke) to match the legend color can be effective for clarity. Use `ax.spines['bottom'].set_linewidth(2)` and `ax.spines['bottom'].set_color('C0')` (or 'C1', etc.) to achieve this.

## Layout

- **Minimize whitespace**. Use `gridspec` with tight `hspace`/`wspace` (0.05-0.15 common).
- Size the figure with the expectation that it will go into a manuscript in 8.5 x 11 letter format. Generally, this either means narrow enough to fit text to the side or taking up the entire width of the available page space.
## Bar and summary plots

- **Overlay individual data points** on bars/means to show the underlying distribution. Use small markers with jitter and slight transparency (e.g., `s=12, alpha=0.7`).
- Include **error bars** (SEM or CI) on summary statistics.

## Rasterization for performance

Identify scatter plots and image overlays with many (>1k) points. These elements produce thousands of vector paths and make SVGs/PDFs slow to render (watch for SVGs exceeding ~10 MB). Ask the user if they'd like to use `rasterized=True` on heavy artists to embed them as bitmaps while keeping text and axes as vectors:

```python
ax.imshow(img, rasterized=True)
ax.scatter(x, y, c=colors, rasterized=True)
```

The `dpi` argument in `savefig` controls the resolution of rasterized elements. Use 600 dpi for publication quality.

## Output

- Always save **PNG** (600 dpi), **SVG**, and **PDF** (all with `dpi=600, bbox_inches='tight', pad_inches=0.1, transparent=False`). If the figure is very large, prompt the user for guidance on DPI.
- Save into **hierarchical subfolders named after the analysis**, e.g., `figures/consistency_curves/barplot_means`.
- SVG is the editable master for Illustrator; PNG is the raster preview.
- Expect figures will be edited in Adobe Illustrator, included in LaTeX manuscripts, and submitted to journals.
- For LaTeX embedding, convert SVG to PDF using the `latex-pdf-preprocess` skill.

## Recommended helper

- Use `bnpm.plotting_helpers.Figure_Saver` when available:
  - `format_save=['svg', 'png']`
  - `svg_fontType='none'`
  - `kwargs_savefig={'dpi': 600, 'bbox_inches': 'tight', 'pad_inches': 0.1, 'transparent': False}`