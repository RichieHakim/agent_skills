---
name: latex-pdf-preprocess
description: Tool for preparing PDF figure files for embedding in LaTeX (e.g., with \includegraphics).
user-invokable: true
---

# LaTeX PDF Figure Preprocessing

Use Ghostscript to normalize a PDF figure so it embeds cleanly in LaTeX.

## Core Command

```bash
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \
  -dCompatibilityLevel=1.6 -dPDFSETTINGS=/prepress \
  -sOutputFile=output.pdf \
  input.pdf
```

Replace `input.pdf` and `output.pdf` with the actual paths. A common convention is to suffix the output with `_latex`:

```bash
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \
  -dCompatibilityLevel=1.6 -dPDFSETTINGS=/prepress \
  -sOutputFile="${input%.pdf}_latex.pdf" \
  "$input"
```

## What This Does

- **`-dCompatibilityLevel=1.6`** — targets PDF 1.6, broadly compatible with pdflatex, xelatex, lualatex
- **`-dPDFSETTINGS=/prepress`** — high-quality output: embeds all fonts, preserves resolution, flattens transparency
- **`-dSAFER -dBATCH -dNOPAUSE`** — non-interactive, safe mode

## Common LaTeX Embedding Errors This Fixes

| Error | Cause | Fixed by |
|-------|-------|---------|
| `PDF inclusion: found PDF version <1.x>, but at most 1.5 allowed` | PDF version too new | `-dCompatibilityLevel=1.6` |
| Transparency artifacts or white boxes | PDF has live transparency | Ghostscript flattens it |
| Missing glyphs / font substitution | Fonts not embedded | `/prepress` embeds all fonts |
| Color space errors (RGB vs CMYK) | Mixed color spaces | Ghostscript normalizes |

## Checking Ghostscript is Available

```bash
which gs && gs --version
```

If not installed:
```bash
brew install ghostscript       # macOS
sudo apt install ghostscript   # Linux
```

## Batch Processing Multiple Figures

```bash
for f in figures/*.pdf; do
  gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \
    -dCompatibilityLevel=1.6 -dPDFSETTINGS=/prepress \
    -sOutputFile="${f%.pdf}_latex.pdf" "$f"
done
```

## Verifying the Output

```bash
# Check PDF version and metadata
pdfinfo output.pdf

# Quick sanity check: page count and size unchanged
pdfinfo input.pdf | grep -E 'Pages|Page size'
pdfinfo output.pdf | grep -E 'Pages|Page size'
```
