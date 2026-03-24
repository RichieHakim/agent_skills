---
name: latex_pdf_preprocess
description: Tool for preparing PDF figure files for embedding in LaTeX (e.g., with \includegraphics).
user-invocable: true
---

# LaTeX PDF Figure Preprocessing

Normalize a PDF figure so it embeds cleanly in LaTeX with pdflatex, xelatex, and lualatex.

## Why two steps?

Ghostscript alone (`pdf -> gs -> pdf`) preserves certain internal PDF structures (indirect object references from Illustrator, transparency groups) that crash **xdvipdfmx** (the PDF backend for xelatex) with:

```
Assertion failed: (!indirect->pf), function write_indirect, file pdfobj.c
```

The fix is to round-trip through PostScript first (`pdf -> pdftops -> ps -> gs -> pdf`). The `pdftops` step strips the problematic structures; the `gs` step then normalizes fonts, color spaces, and PDF version.

## Core Command

```bash
pdftops input.pdf /tmp/_latex_preprocess.ps
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \
  -dCompatibilityLevel=1.4 \
  -dPDFSETTINGS=/prepress \
  -sOutputFile=output.pdf \
  /tmp/_latex_preprocess.ps
rm /tmp/_latex_preprocess.ps
```

- **`-dCompatibilityLevel=1.4`** — PDF 1.4, compatible with all TeX engines
- **`-dPDFSETTINGS=/prepress`** — high quality: embeds all fonts, preserves resolution
- Output is saved as `<name>_latex.pdf` alongside the original

## Batch Processing

```bash
for f in figures/*/figure.pdf; do
  out="${f%.pdf}_latex.pdf"
  pdftops "$f" /tmp/_lpp.ps && \
  gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \
    -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress \
    -sOutputFile="$out" /tmp/_lpp.ps && \
  rm /tmp/_lpp.ps && \
  echo "OK: $out" || echo "FAIL: $f"
done
```

## Dependencies

Requires `poppler-utils` (for `pdftops`) and `ghostscript` (for `gs`):
```bash
brew install poppler ghostscript   # macOS
sudo apt install poppler-utils ghostscript  # Linux
```

Check they're installed:
```bash
which pdftops gs && gs --version
```

## Verifying the Output

```bash
# Check PDF version is 1.4 and page dimensions are preserved
pdfinfo output.pdf | grep -E 'PDF version|Pages|Page size'
```

## Common Errors This Fixes

| Error | Cause | Fixed by |
|-------|-------|----------|
| `Assertion failed: (!indirect->pf)` in xdvipdfmx | Illustrator indirect object refs | PostScript roundtrip strips them |
| `PDF inclusion: found PDF version <1.x>, but at most 1.5 allowed` | PDF version too new | `-dCompatibilityLevel=1.4` |
| Transparency artifacts or white boxes | Live transparency | `pdftops` flattens it |
| Missing glyphs / font substitution | Fonts not embedded | `/prepress` embeds all fonts |
