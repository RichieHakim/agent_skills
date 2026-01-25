---
name: read-scientific-pdfs-mineru
description: Extract scientific PDFs to lossless Markdown using MinerU. Assumes a pre-existing conda env named "mineru".
---

# read-scientific-pdfs-mineru

Goal: convert PDFs to Markdown as losslessly as possible (no summarization). This skill assumes a conda env named `mineru` already exists. If it doesn’t, **stop** and tell the user what is missing (create the env + install MinerU) and do not attempt installs.

## Method differences (choose based on PDF type)
- `txt`: Use for digital PDFs with selectable text. Fastest and most faithful for journals/preprints.
- `ocr`: Use for scanned PDFs or image-only PDFs. Slower; OCR errors are possible.
- `auto`: Let MinerU choose. Good when you’re unsure, but `txt` is usually best for scientific papers.

## Quick use
```bash
conda activate mineru
python skills/read-scientific-pdfs-mineru/scripts/mineru_extract.py \
  --filepath_pdf /path/to/paper.pdf \
  --output_dir agent_assets/<project_name>/pdf_conversions \
  --method txt
```

## Default execution mode: dispatch via sbatch
Use Slurm by default. Follow `AGENTS.md` for partition/cpu/mem/account values. Create a small dispatch script in `agent_assets/<project_name>/code/` and submit it.

Example `agent_assets/<project_name>/code/mineru_dispatch.sbatch`:
```bash
#!/usr/bin/env bash
#SBATCH --account=<account_name_from_AGENTS>
#SBATCH --time=0-02:00:00
#SBATCH --partition=<partition_from_AGENTS>
#SBATCH --gres=gpu:1
#SBATCH -c <cpu_from_AGENTS>
#SBATCH --mem=<mem_from_AGENTS>
#SBATCH --output=agent_assets/<project_name>/artifacts/mineru_%j.out
#SBATCH --error=agent_assets/<project_name>/artifacts/mineru_%j.err

set -euo pipefail

conda activate mineru

python skills/read-scientific-pdfs-mineru/scripts/mineru_extract.py \
  --filepath_pdf /path/to/paper.pdf \
  --output_dir agent_assets/<project_name>/pdf_conversions \
  --method txt
```

Submit with:
```bash
sbatch agent_assets/<project_name>/code/mineru_dispatch.sbatch
```

## If the user explicitly asks to use a compute node (interactive)
SSH to the node in `AGENTS.md`, activate `mineru`, then run the script:
```bash
ssh <compute_node_name>
conda activate mineru
python skills/read-scientific-pdfs-mineru/scripts/mineru_extract.py \
  --filepath_pdf /path/to/paper.pdf \
  --output_dir agent_assets/<project_name>/pdf_conversions \
  --method txt
```

## Script behavior
- Refuses to run unless the active conda env is named `mineru`.
- Refuses to run if the `mineru` CLI is missing from PATH.
- Writes results to the provided `--output_dir`.
- Prints the paths of all extracted `.md` files.
- Optional: `--preview-lines N` to print the first N lines of each `.md` for quick context loading.

## Recommended output layout
Use `agent_assets/<project_name>/pdf_conversions/` so outputs are easy to find and reuse.

## Seamless handoff (read Markdown into context)
After extraction, open the printed `.md` file and read it into context. If multiple `.md` files were produced, pick the one matching the PDF basename.

Example:
```bash
sed -n '1,200p' agent_assets/<project_name>/pdf_conversions/<basename>/<subdir>/<basename>.md
```

## If something is missing
If `conda activate mineru` fails or MinerU isn’t on PATH, tell the user what to create/install and stop.

## Throughput (rough guidance)
On GPU nodes, digital PDFs tested so far averaged ~24–53 seconds per page (short papers were slower per page). Expect variability by hardware, PDF layout complexity, and chosen method.

## Safety
Never upload PDFs to external services without explicit approval.
