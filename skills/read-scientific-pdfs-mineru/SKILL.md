---
name: read-scientific-pdfs-mineru
description: Extract scientific PDFs to lossless Markdown using MinerU. Assumes a pre-existing conda env named "mineru".
---

# read-scientific-pdfs-mineru

Goal: convert PDFs to Markdown as losslessly as possible (no summarization). This skill assumes a conda env named `mineru` already exists. If it doesn’t, **stop** and tell the user what is missing (create the env + install MinerU) and do not attempt installs.

## PDF placement
Save the source PDF under `agent_assets/<project_name>/artifacts/pdf_conversions/` before extraction. Use the same basename throughout the conversion outputs.

## Method differences (choose based on PDF type)
- `txt`: Use for digital PDFs with selectable text. Fastest and most faithful for journals/preprints.
- `ocr`: Use for scanned PDFs or image-only PDFs. Slower; OCR errors are possible.
- `auto`: Let MinerU choose. Good when you’re unsure, but `txt` is usually best for scientific papers.

## Quick use
```bash
SKILLS_DIR="$(readlink -f .agent/skills)"
conda activate mineru
python "$SKILLS_DIR/read-scientific-pdfs-mineru/scripts/mineru_extract.py" \
  --filepath_pdf agent_assets/<project_name>/artifacts/pdf_conversions/<paper>.pdf \
  --output_dir agent_assets/<project_name>/pdf_conversions \
  --method txt
```

If `.agent/skills` is unavailable, set `SKILLS_DIR` to your central skills checkout (e.g., `$CODEX_HOME/skills`) and reuse the same command.

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

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate mineru

SKILLS_DIR="$(readlink -f .agent/skills)"
python "$SKILLS_DIR/read-scientific-pdfs-mineru/scripts/mineru_extract.py" \
  --filepath_pdf agent_assets/<project_name>/artifacts/pdf_conversions/<paper>.pdf \
  --output_dir agent_assets/<project_name>/pdf_conversions \
  --method txt
```

Submit with:
```bash
sbatch agent_assets/<project_name>/code/mineru_dispatch.sbatch
```

## Local fallback (no sbatch)
If the PDF is small and you already have an interactive compute node, run the “Quick use” command directly. This avoids waiting for Slurm scheduling.

## If the user explicitly asks to use a compute node (interactive)
SSH to the node in `AGENTS.md`, activate `mineru`, then run the script:
```bash
ssh <compute_node_name>
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate mineru
SKILLS_DIR="$(readlink -f .agent/skills)"
python "$SKILLS_DIR/read-scientific-pdfs-mineru/scripts/mineru_extract.py" \
  --filepath_pdf agent_assets/<project_name>/artifacts/pdf_conversions/<paper>.pdf \
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

## Output sanity check
After completion, confirm extraction:
```bash
find agent_assets/<project_name>/pdf_conversions -type f -name "*.md"
```

## Streamlined error feedback
- Check job state: `squeue -j <jobid>`
- Stream logs: `tail -f agent_assets/<project_name>/artifacts/mineru_<jobid>.err`
- If `.err` is empty, also check `.out`.

## Seamless handoff (read Markdown into context)
After extraction, open the printed `.md` file and read it into context. If multiple `.md` files were produced, pick the one matching the PDF basename.

Example:
```bash
sed -n '1,200p' agent_assets/<project_name>/pdf_conversions/<basename>/<subdir>/<basename>.md
```

## If something is missing
If `conda activate mineru` fails or MinerU isn’t on PATH, tell the user what to create/install and stop.

## Throughput (rough guidance)
On GPU nodes, digital PDFs tested so far averaged ~20–60 seconds per page (short papers are slower per page). Expect variability by hardware, PDF layout complexity, and chosen method.

## Safety
Never upload PDFs to external services without explicit approval.
