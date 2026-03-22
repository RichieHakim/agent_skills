---
name: latex_pdf_preprocess
description: Tool for preparing PDF figure files for embedding in LaTeX (e.g., with \includegraphics).
user-invocable: true
---

# LaTeX PDF Figure Preprocessing

Normalize a PDF figure so it embeds cleanly in LaTeX with both xelatex and lualatex.

## Core Command

Always run both steps in sequence. The PostScript roundtrip flattens transparency (which crashes xelatex), and the Ghostscript pass normalizes fonts, color spaces, and PDF version.

```bash
pdftops input.pdf - | ps2pdf -dPDFSETTINGS=/prepress - input.pdf
```

## Batch Processing

```bash
for f in figures/*.pdf; do
  pdftops "$f" - | ps2pdf -dPDFSETTINGS=/prepress - "${f%.pdf}_tmp.pdf"
  mv "${f%.pdf}_tmp.pdf" "$f"
done
```

## Dependencies

Requires `poppler-utils` and `ghostscript`:
```bash
brew install poppler ghostscript   # macOS
sudo apt install poppler-utils ghostscript  # Linux
```

## Verifying the Output

```bash
pdfinfo input.pdf | grep -E 'Pages|Page size'
pdfinfo output.pdf | grep -E 'Pages|Page size'
```
