---
name: matplotlib-figure-editing
description: Use this skill when the user wants to edit, reformat, or add panels to existing scientific figures exported as PDF/SVG (e.g., from matplotlib or Adobe Illustrator). This includes: extracting data from SVG paths to recreate plots, placing formatted matplotlib panels onto an existing PDF, removing unformatted panels, coordinate calibration from SVG tick positions, and parsing SVG fill-between polygons.
---

# Matplotlib Figure Editing Guide

Workflow for adding or replacing formatted panels in an existing PDF figure that was originally exported from matplotlib (possibly via Illustrator as SVG/AI/PDF).

## Overview

1. Parse the SVG to extract data from embedded matplotlib paths
2. Calibrate coordinates using SVG tick label positions
3. Recreate panels in matplotlib with matching style
4. Use PyMuPDF (fitz) to redact old panels and overlay new ones

## Environment Setup

```bash
# Use the project's conda env directly (avoid conda run which may invoke system Python)
/path/to/miniconda3/envs/prod/bin/python3 script.py

# Install dependencies in the env
/path/to/miniconda3/envs/prod/bin/pip install pymupdf matplotlib
```

## SVG Structure

Matplotlib exports SVG groups with IDs like `figure_1`, `figure_1-2`, etc. Each axes group contains:
- `line2d_N` — mean/data lines (path with `M x,y l dx,dy,...`)
- `FillBetweenPolyCollection_N` — fill_between error bands
- Text elements for tick labels, axis labels, titles

### Finding Panel Groups

```python
import xml.etree.ElementTree as ET

tree = ET.parse('figure.svg')
root = tree.getroot()

# List top-level group IDs
for e in root.iter():
    gid = e.get('id', '')
    if gid and gid.startswith('figure'):
        print(gid)
```

### Extracting Path Data

```python
def get_path_d(root, elem_id, path_index=0):
    for e in root.iter():
        if e.get('id', '') == elem_id:
            paths = [c for c in e.iter() if c.tag.split('}')[-1] == 'path']
            if paths and path_index < len(paths):
                return paths[path_index].get('d', '')
    return ''
```

## Parsing SVG Paths

### Mean Line (`M x,y l dx,dy,...`)

```python
import re

def parse_rel_line(d_str):
    """Parse 'M x0,y0 l dx1,dy1, ...' → list of absolute (x,y)."""
    m = re.match(r'M([\d.\-]+),([\d.\-]+)', d_str)
    if not m:
        return []
    x, y = float(m.group(1)), float(m.group(2))
    pts = [(x, y)]
    rest = d_str[m.end():]
    l_m = re.search(r'l\s*(.*)', rest)
    if l_m:
        nums = re.findall(r'[-+]?\d*\.?\d+', l_m.group(1))
        for i in range(0, len(nums) - 1, 2):
            x += float(nums[i]); y += float(nums[i + 1]); pts.append((x, y))
    return pts
```

### Fill-Between Error Band Polygon

The matplotlib `fill_between` polygon has this structure:
```
M x0,y_upper_first        ← starting corner (upper bound at rank_min)
v dy                      ← drop to lower bound (rank_min)
l dx,dy ...               ← lower bounds going right (rank_min+step .. rank_max)
v -dv                     ← rise to upper bound (rank_max) — turnaround
h 0 (optional)
l -dx,dy ...              ← upper bounds going left (rank_max-step .. rank_min+step)
Z                         ← close (back to starting corner)
```

**Critical bug to avoid:** The polygon's `l` going left ends one step short of the starting corner because `Z` closes it. Always exclude the last element of the reversed upper bound list:

```python
def parse_fillbetween_polygon(d_str):
    """Returns (upper_ys, lower_ys) ordered left→right (rank_min to rank_max)."""
    tokens = re.findall(r'[MLlHhVvZz]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d_str)
    verts = []
    x = y = 0.0
    cmd = None
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in 'MmLlHhVvZz':
            cmd = t; i += 1; continue
        val = float(t)
        if cmd == 'M':
            x = val; i += 1; y = float(tokens[i]); verts.append(('M', x, y)); i += 1
        elif cmd == 'm':
            x += val; i += 1; y += float(tokens[i]); verts.append(('m', x, y)); i += 1
        elif cmd == 'L':
            x = val; i += 1; y = float(tokens[i]); verts.append(('L', x, y)); i += 1
        elif cmd == 'l':
            x += val; i += 1; y += float(tokens[i]); verts.append(('l', x, y)); i += 1
        elif cmd in ('H', 'h'):
            x = val if cmd == 'H' else x + val
            verts.append(('h', x, y)); i += 1
        elif cmd in ('V', 'v'):
            y = val if cmd == 'V' else y + val
            verts.append(('v', x, y)); i += 1
        else:
            i += 1

    going_right = None
    lower_ys = []
    upper_ys_rev = []
    upper_start_y = None
    upper_end_y = None

    for j, (vtype, vx, vy) in enumerate(verts):
        if j == 0:
            upper_start_y = vy; continue
        prev_vx = verts[j - 1][1]
        dx = vx - prev_vx

        if going_right is None:
            if abs(dx) < 1e-6:
                lower_ys.append(vy); going_right = True
            continue

        if going_right:
            if dx > 0:
                lower_ys.append(vy)
            elif abs(dx) < 1e-6:
                if vy < lower_ys[-1]:
                    upper_end_y = vy; going_right = False
        else:
            if dx < 0:
                upper_ys_rev.append(vy)

    # IMPORTANT: exclude last element (closing vertex ≈ starting corner duplicate)
    upper_ys = [upper_start_y] + upper_ys_rev[:-1][::-1]
    if upper_end_y is not None:
        upper_ys.append(upper_end_y)

    return upper_ys, lower_ys
```

## Coordinate Calibration

Read SVG tick label positions (inspect with a browser or XML parser) and fit a linear map:

```python
# Example: y-axis calibration
svg_y_ticks = [240.19, 232.13, 224.07, 216.01, 207.94]  # SVG y positions of tick marks
data_values  = [-1.0,   -0.8,   -0.6,   -0.4,   -0.2]   # corresponding data values

y0    = svg_y_ticks[0]
dy_sv = svg_y_ticks[0] - svg_y_ticks[-1]   # SVG delta (positive; SVG Y flips)
dy_dv = data_values[-1] - data_values[0]   # data delta

def svg_y_to_data(svg_y):
    return data_values[0] + (y0 - svg_y) / dy_sv * dy_dv

# Example: x-axis calibration
svg_x_ticks = [117.87, 134.93, 151.36, 172.58, 194.03]
data_x       = [2, 6, 10, 15, 20]

a = (svg_x_ticks[-1] - svg_x_ticks[0]) / (data_x[-1] - data_x[0])
b = svg_x_ticks[0] - a * data_x[0]

def svg_x_to_data(svg_x):
    return (svg_x - b) / a
```

## Matplotlib Style Matching Published Panels

```python
from matplotlib import rcParams

rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.labelsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'axes.titlesize': 8,
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'lines.linewidth': 0.75,
    'lines.markersize': 2.5,
    'legend.fontsize': 8,
    'legend.frameon': False,
    'pdf.fonttype': 42,  # embed fonts as TrueType
})
```

### Panel Label Positioning

Place panel labels (A, B, C, D...) at the top-left of each axes:

```python
ax.text(-0.28, 1.18, 'D', transform=ax.transAxes,
        fontsize=10, fontweight='bold', va='top', ha='left')
```

Adjust x-offset based on y-axis label width (more negative = further left).

### Right-Side Inline Line Labels (avoid legend overlap)

```python
# Extend x-axis range to make room for labels
ax.set_xlim(1, 28)   # data ends at 20, labels start at 20.4

# Place labels at rightmost data point y-values
ax.text(20.4, y_freq[-1],  'freq.',    color='#1f77b4', va='center', ha='left', fontsize=7)
ax.text(20.4, y_temp[-1],  'temporal', color='#ff7f0e', va='center', ha='left', fontsize=7)
ax.text(20.4, y_pts[-1],   'points',   color='#2ca02c', va='center', ha='left', fontsize=7)
```

## PDF Overlay with PyMuPDF

```python
import fitz  # pip install pymupdf
import io

# Save matplotlib figure to in-memory PDF buffer
buf = io.BytesIO()
fig.savefig(buf, format='pdf', bbox_inches='tight')
buf.seek(0)
plt.close(fig)

# Open the target PDF
doc = fitz.open('figure.pdf')
page = doc[0]

# Redact (erase) old panels — removes both text and vector graphics
redact_rects = {
    'panel_old': fitz.Rect(x0, y0, x1, y1),   # PDF points, origin top-left
}
for name, rect in redact_rects.items():
    page.add_redact_annot(rect, fill=(1, 1, 1))  # white fill
page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

# Overlay new panel
panel_rect = fitz.Rect(x0, y0, x1, y1)    # where to place the new panel
doc_panel = fitz.open("pdf", buf.read())
page.show_pdf_page(panel_rect, doc_panel, 0)
doc_panel.close()

doc.save('figure_edited.pdf', garbage=4, deflate=True)
doc.close()
```

### PDF Coordinate System

- Origin at **top-left** of page, Y increases **downward**
- Page sizes in points: Letter = 612×792, A4 = 595×842
- SVG units approximate PDF points (may need scale factor if figure doesn't fill page)
- To find where SVG elements map to PDF coordinates, compare SVG tick positions to known PDF regions

### Finding Correct Redaction Rects

The easiest way to find coordinates of panels to remove:
1. Open the PDF in a viewer, note approximate pixel coordinates
2. Convert: for a 612×792pt page displayed at some DPI, pixel → point = pixel × 72/display_dpi
3. Or: use pdfplumber to inspect text positions

```python
import pdfplumber
with pdfplumber.open('figure.pdf') as pdf:
    page = pdf.pages[0]
    for word in page.extract_words():
        if 'BIC' in word['text']:
            print(word)   # shows x0, y0, x1, y1 in PDF points
```

## Notes and Pitfalls

- **Never use Unicode subscripts/superscripts** (₀¹²...) in matplotlib text — use `<sub>/<super>` tags in reportlab, or ASCII like `(1e9)` in matplotlib
- **tight_layout + bbox_inches='tight'** captures out-of-axes elements (panel labels, offset text)
- **SVG group IDs** follow the pattern `figure_1`, `figure_1-2`, `figure_1-5`, etc. (not sequential — the suffix comes from matplotlib's internal counter)
- **Fill-between polygon**: the closing `Z` command returns to the starting corner without adding a duplicate vertex, so the `l` going left has N-1 points for N data points on each half — always slice with `[:-1]` before reversing
- **conda run picks system Python** on some setups; always invoke the env Python directly: `/path/to/envs/NAME/bin/python3`
