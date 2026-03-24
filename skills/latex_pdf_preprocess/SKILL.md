---
name: latex_pdf_preprocess
description: Tool for preparing PDF figure files for embedding in LaTeX (e.g., with \includegraphics).
user-invocable: true
---

# LaTeX PDF Figure Preprocessing

Fix PDF figures (especially from Adobe Illustrator) so they embed cleanly in xelatex.

## The problem

Adobe Illustrator exports PDFs with ICC-based color profiles as indirect stream references inside page-level transparency groups. **xdvipdfmx** (xelatex's PDF backend) crashes on these:

```
Assertion failed: (!indirect->pf), function write_indirect, file pdfobj.c
```

## The fix

Replace the ICC color space reference in the page-level transparency `/Group` with `/DeviceRGB`. This is a single metadata swap — no rasterization, no PostScript roundtrip, no content changes. Transparency and blending are fully preserved.

## Core Command

```python
import pikepdf, sys

pdf = pikepdf.open(sys.argv[1])
for page in pdf.pages:
    if "/Group" in page:
        g = page["/Group"]
        if "/CS" in g and isinstance(g["/CS"], pikepdf.Array):
            g["/CS"] = pikepdf.Name("/DeviceRGB")
pdf.save(sys.argv[2])
```

Usage:
```bash
python3 fix_pdf.py input.pdf output.pdf
```

## Batch Processing

```python
import pikepdf, os

for d in sorted(os.listdir("figures")):
    fpath = os.path.join("figures", d, "figure.pdf")
    if not os.path.isfile(fpath):
        continue
    pdf = pikepdf.open(fpath)
    fixed = False
    for page in pdf.pages:
        if "/Group" in page:
            g = page["/Group"]
            if "/CS" in g and isinstance(g["/CS"], pikepdf.Array):
                g["/CS"] = pikepdf.Name("/DeviceRGB")
                fixed = True
    if fixed:
        tmp = fpath + ".tmp"
        pdf.save(tmp)
        pdf.close()
        os.replace(tmp, fpath)
        print(f"Fixed: {d}")
    else:
        pdf.close()
        print(f"OK:    {d} (no ICC group)")
```

## Dependencies

```bash
pip install pikepdf
```

## Verifying the Output

```bash
# Page dimensions should be identical
pdfinfo input.pdf | grep 'Page size'
pdfinfo output.pdf | grep 'Page size'
```

Or confirm the fix programmatically:
```python
import pikepdf
pdf = pikepdf.open("output.pdf")
for page in pdf.pages:
    if "/Group" in page and "/CS" in page["/Group"]:
        cs = page["/Group"]["/CS"]
        assert cs == pikepdf.Name("/DeviceRGB"), f"Still ICC: {cs}"
print("OK")
```

## What this does NOT do

- Does not rasterize anything — vectors, images, and text are untouched
- Does not change PDF version
- Does not flatten transparency — blending modes and opacity are preserved
- Does not touch Form XObject groups (only the page-level group needs fixing)

## Background

The page-level `/Group` dictionary controls the transparency blending color space for the entire page. Illustrator sets this to `[/ICCBased <stream>]` where the stream is an embedded sRGB ICC profile. xdvipdfmx crashes when it encounters this indirect stream reference during PDF output. Replacing it with the equivalent `/DeviceRGB` name avoids the indirect reference while preserving identical color behavior (the ICC profile is sRGB).
