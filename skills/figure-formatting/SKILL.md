---
name: figure-formatting
description: Guide for styling scientific figures with matplotlib.
user-invocable: true
---

# Figure Formatting

Style guide for generating publication-ready scientific figures with matplotlib. These conventions match the visual language of the face-rhythm manuscript and should be applied to all new figures.

## Typography

- **Font**: Arial only. Note: On Linux where Arial is unavailable, use `"Nimbus Sans"` as the rendering font (identical metrics), then post-process SVGs to replace with Arial:
  ```python
  svg_text = Path("figure.svg").read_text()
  svg_text = svg_text.replace("Nimbus Sans", "Arial")
  Path("figure.svg").write_text(svg_text)
  ```
- **Minimum size**: 8 pt normal-weight for all text including tick labels, axis labels, legends, and annotations. Never use font sizes smaller than 8 pt; if text doesn't fit, consider how to abbreviate, rotate, remove, or redesign the text or panel layout.
- **Panel titles**: ~10 pt, bold, lowercase except for acronyms (e.g., PCA, EVR, BMI, etc.). 
- **Sub-panel titles**: 8 pt, normal weight.
- **Units**: parenthesized after label, e.g., `frequency (Hz)`, `time (s)`, `(a.u.)`.

## Panel labels

Every multi-panel figure must have panel labels. Add them automatically whenever a figure has more than one axes panel.

- **Main panel labels**: uppercase bold letters (A, B, C, …), 16 pt, Arial, bold. Place close to and near the top-left of each panel. Panel labels should be aligned across panels in the same row and column.
- **Subpanel labels**: when a panel contains subdivisions, label them as e.g. **B(i)**, **B(ii)**, **B(iii)**, **B(iv)**. The letter remains 16 pt bold; the roman numeral suffix is 8 pt, normal weight. Make a judgement call on whether to use subpanel labels; referencing 'left' and 'right' subpanels is often sufficient and avoids clutter.

For simple layouts, `ax.transAxes` works:
```python
for ax, label in zip(axes, ['A', 'B', 'C']):
    ax.text(-0.12, 1.18, label, transform=ax.transAxes,
            fontsize=16, fontweight='bold', va='top', ha='left',
            fontfamily='Arial')
```

For complex layouts with nested gridspecs, use figure coordinates after rendering:
```python
fig.canvas.draw()
pos = ax.get_position()
fig.text(pos.x0 - 0.03, pos.y1 + 0.02, "A",
         fontsize=16, fontweight='bold', va='top', ha='left',
         fontfamily='Arial')
```

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
- Generally don't use gridlines unless there is a good reason.
- **Axis ranges:** Strongly consider whether to bound the x/y axis ranges to more meaningful limits (e.g., 0 to 1, -100% to 100%, etc.) 

## Lines

- Default line width: 1 pt
- Use solid lines. Avoid dashed lines.
- When overlaying two methods/conditions, try to differentiate with color and reduce opacity of the secondary trace (~0.7) rather than using dashes.

## Transparency and opacity

- Use alpha/transparency **sparingly**. It is difficult to increase opacity post-hoc in Illustrator.

## Colormaps and normalization

- Use **perceptually uniform** colormaps (e.g., `viridis`) unless there is a strong reason not to. Dichromatic colormaps are also good.
- For comparison across panels, use **shared normalization** (same `vmin`/`vmax`). Document if per-panel normalization is used.

## Images and spatial maps

- For scientific images, brighten and oversaturate slightly (`np.clip(img * 1.8, 0, 255)`) for visibility.
- Crop images using `set_xlim` / `set_ylim` rather than array slicing (preserves coordinate alignment with scatter data).
- When reference images consider whether to use `rasterized=True`.
- When images represent different methods/conditions, adding a colored border (spine stroke / border line) to match the legend color can be effective for clarity.

## Line plots

- Aim for a clean look. Generally, avoid point markers unless there is good reason.
- For statistics: Include each sample line (thin, transparent) as well as summary lines (thick, opaque) and use shaded errorbars without a stroke/border. For example, use `ax.fill_between(x, mean - std, mean + std, color='C0', alpha=0.3, linewidth=0)`. Decide between SEM, STD, and CI.

## Bar and summary plots

- **Overlay individual data points** on bars/means to show the underlying distribution. Use small markers with jitter and slight transparency (e.g., `s=12, alpha=0.7`).
- Reduce whitespace aggressively. Bars should be close together.
- Error bars should be a single 2 pt thickness vertical line with no cap.
- Include error bars (SEM or CI) on summary statistics, and variance bars (STD) for more raw data statistics.

## Legend placement

- For legends with many entries that would overlap data, place below, to the side, or in a low-data region of the plot. For precise placement, you can use `bbox_to_anchor` with axes-fraction coordinates.

## Layout

- **Minimize whitespace**. Use `gridspec` with tight `hspace`/`wspace` (0.05-0.15 common).
- Size the figure with the expectation that it will go into a manuscript in 8.5 x 11 letter format. Generally, this either means narrow enough to fit text to the side or taking up the entire width of the available page space.
- **Figure size vs. text size**: `figsize` controls the plot area in inches; `rcParams` text sizes are absolute in points. Changing `figsize` doesn't change the text size.
- To make a panel shorter than its gridspec allocation, you can use a nested subgridspec with an invisible spacer:
  ```python
  gs_inner = gs[0, 2].subgridspec(2, 1, height_ratios=[0.7, 0.3], hspace=0.0)
  ax = fig.add_subplot(gs_inner[0, 0])
  ax_spacer = fig.add_subplot(gs_inner[1, 0]); ax_spacer.axis("off")
  ```
- For square or fixed-ratio panels, you can use `ax.set_box_aspect(1.0)` (or `0.75` for 25% shorter, etc.).
- Get creative with layout! Don't be afraid to break out of the standard grid and use `fig.add_axes` for custom placements. Just make sure to maintain consistent styling and alignment.

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
- After every render, visually inspect for correctness, layout, and style. Common issues include whitespace, overlapping text, and misaligned panels. Debug in a loop a few times until the figure looks right or ask for help if you're stuck.
- SVG is the editable master for Illustrator; PNG is the raster preview.
- Expect figures will be edited in Adobe Illustrator, included in LaTeX manuscripts, and submitted to journals.
- For LaTeX embedding, convert SVG to PDF using the `latex-pdf-preprocess` skill.
- If a PDF has excess whitespace (e.g., from Illustrator artboard being larger than artwork), crop with `pdfcrop --margins 2 input.pdf output.pdf` (margin in bp, 1bp = 1/72 inch).
- If possible, prepare the data used in the figure and plotting code to allow for portability and easy regeneration in the future.

## Recommended helper

- Use `bnpm.plotting_helpers.Figure_Saver` when available:
  - `format_save=['svg', 'png']`
  - `svg_fontType='none'`
  - `kwargs_savefig={'dpi': 600, 'bbox_inches': 'tight', 'pad_inches': 0.1, 'transparent': False}`
