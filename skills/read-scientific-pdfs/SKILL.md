---
name: read-scientific-pdfs
description: Extract, parse, and interpret scientific paper PDFs into structured text, metadata, sections, and references. Use when Codex needs to read or summarize scholarly PDFs (multi-column articles), recover title/authors/abstract/sections/citations, or convert papers to clean Markdown/JSON. Prefer a modern scholarly model like Nougat (academic PDF to Markdown), with fallbacks to pdfplumber/PyMuPDF and OCR for scans.
---

# read-scientific-pdfs

Act as a research-paper PDF reader. Prioritize structure (title, authors, abstract, sections, references) and preserve section order.

## Preferred tooling (use these first)
- Use Nougat (Neural Optical Understanding for Academic Documents) for PDF-to-Markdown/LaTeX extraction.
- Use the helper script in `scripts/nougat_extract.py`.

## Compute/cluster notes (portable)
- Follow the repo's `AGENTS.md` for the current compute node, conda env, and partition/resource defaults. Do not hard-code those values here.
- Run Nougat on a compute node (not login) via `sbatch` per `AGENTS.md`.
- If VRAM is limiting, choose the higher-VRAM partition indicated in `AGENTS.md` and keep Nougat batch size at 1.
- Add a quick GPU preflight in batch runs (e.g., `nvidia-smi`, `echo $CUDA_VISIBLE_DEVICES`) and fail fast if no GPU is available.

## Quick workflow
1. Check whether the PDF is text-based or scanned (is text selectable?).
2. Run Nougat to extract Markdown (good for math + tables).
3. If Nougat fails (missing pages, non-Latin scripts, off-domain), fallback to text extraction with pdfplumber/PyMuPDF.
4. If scanned: run OCR (ocrmypdf + tesseract), then repeat steps 2-3.

Fallbacks are manual: the Nougat helper script does not automatically switch tools.

## Helper script
- `scripts/nougat_extract.py` runs the local Nougat CLI and writes Markdown outputs.

Example:
```bash
python scripts/nougat_extract.py \
  --pdf /path/to/paper.pdf \
  --out /path/to/nougat_out
```

## Output expectations
- Cite section headers (and page numbers if available) when summarizing.
- Preserve multi-column order; spot-check section transitions.
- Keep references in a dedicated section.

## Quality checks
- Compare extracted abstract with the PDF first page to ensure proper ordering.
- If Nougat reports missing pages, rerun with `--no-skipping` or fallback to text extraction.
- If headings are missing, fallback to pdfplumber/PyMuPDF and rebuild headings via regex + font-size heuristics.
- If math/figures are critical, extract figure captions and equation blocks separately.

## Postprocess cleanup (optional, no content changes)
- Always keep the raw `.mmd` output; write cleaned output to a separate file.
- Only apply non-destructive cleanup (no paraphrasing or reformatting of meaning):
  - Remove exact consecutive duplicate lines (e.g., repeated footnotes).
  - Collapse obvious repeated token spam in metadata blocks (e.g., long runs of `addr1`).
  - Normalize excessive blank lines or whitespace.
  - Preserve all section headers, equations, references, and figure captions.
- If a file is mostly `[MISSING_PAGE_EMPTY:*]` or is a figure-only PDF, keep it as-is and flag it.

## Context management
- If the platform supports subagents, delegate large batch cleanup/QA to a subagent to keep the main thread light.
- If subagents are not available, emulate this by running cleanup scripts and writing a short summary to `agent_assets/` rather than pasting large outputs into the main thread.

## Known limitations (Nougat vs alternatives)
- Figures/diagrams/plots are not reconstructed; only captions are reliably extracted.
- Tables are linearized and can lose alignment; verify against the PDF when precision matters.
- Multi-column ordering can still drift on complex layouts.
- Scanned PDFs require OCR first; OCR errors propagate into Nougat.
- Plain text extractors are better for quick/cheap text but lose structure.

## Fallback stack
- Text extraction: pdfplumber or PyMuPDF (fitz).
- Layout/segmentation: layoutparser or unstructured (if available).
- OCR: ocrmypdf + tesseract.

## Safety
- Never upload PDFs to remote services without explicit user approval.
