---
name: scientific_figure_export
description: Best practices for exporting scientific figures (SVG/PNG) for Illustrator editing, including fonts, DPI, and folder structure.
---

# Scientific Figure Export

Use this skill when saving figures. These are opinionated defaults to keep files editable and publication-ready.

## Downstream use
- Expect that figures will be edited in Adobe Illustrator, included in latex manuscripts, saved as PDFs, and submitted to scientific journals with design standards.

## Save formats
- Always save **SVG + PNG**.
- SVG is the editable master; PNG is the raster preview / export.
- Set **SVG text to editable** (matplotlib: `svg.fonttype = 'none'`).

## Fonts
- Use **Arial** as the default font family.
- Keep font sizes consistent across panels; avoid tiny text. Most figures will become small panels in a larger figure, and text will be scaled to at least 8pt in the final figure.

## Raster quality
- For PNG exports, use **>= 450 DPI** (prefer 600 DPI when file size permits). If figure is very large, prompt user for guidance.
- If a plot is very dense (e.g. scatter plot with many points that would result in >~10MB SVG), prompt user to consider setting `rasterized=True` for that artist so the SVG stays light but text remains vector.

## Transparency & opacity
- Use alpha/transparency sparingly. It is difficult to increase opacity post-hoc in Illustrator.

## Colormaps & normalization
- Use perceptually uniform colormaps (e.g., `viridis`) unless there is a strong reason not to. Dichromatic colormaps are great. Use the appropriate class of colormap for the problem.
- For comparison across panels, use **shared normalization** (same vmin/vmax). Document if per-panel normalization is used.

## Folder structure
- Save into **hierarchical subfolders named after the analysis**, e.g.:
  - `figures/consistency_curves/barplot_means`
  - `figures/consistency_curves/barplot_medians`
  - `figures/consistency_curves/scatter_by_mouse`

## Recommended helper
- Look into using the `bnpm.plotting_helpers` module for figure making and saving. Read relevant docstrings and examples.
- Use `bnpm.plotting_helpers.Figure_Saver`:
  - `format_save=['svg', 'png']`
  - `svg_fontType='none'`
  - `kwargs_savefig={'dpi': 600, 'bbox_inches': 'tight', 'pad_inches': 0.1, 'transparent': False}`

## Minimal Matplotlib config
```
import matplotlib as mpl
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['svg.fonttype'] = 'none'
```
