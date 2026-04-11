---
name: notebook-to-script
description: Refactor an exploratory Jupyter notebook into a single runnable Python script while preserving the scientific "meat". Use when converting an .ipynb to a standalone script for batch/HPC execution.
---

# Notebook to Script

Treat the notebook as a **prototype spec**. Your job is to extract the scientific logic and wrap it in a standalone script that follows `script-opinions`.

**Prerequisite:** load `script-opinions` for style, logging, run-dir, and skeleton rules. This skill covers only the *conversion protocol*.

## Output contract

- Return **one** runnable Python script in a single code block.
- Do **not** output a worker/sbatch shell script unless explicitly requested (see the `job-dispatch` skill, if needed).
- Preserve scientific logic as-is. Refactor aggressively *around* it, not through it.

## Protocol

### 1) Ingest
Convert `.ipynb` to script text via the bundled `scripts/notebook_ingest.py` or `jupyter nbconvert --to script`. Read the result into context before reasoning.

### 2) Audit — objective, I/O, hidden state, hazards
- **Objective** — one sentence.
- **Inputs / outputs** — files, dirs, env-vars, formats; what's written and where.
- **Hidden state** — globals mutated across cells, implicit CWD, `sys.path.append`, cells that depend on earlier cells being run manually, variables carried from a prior kernel, relative paths assuming the notebook's CWD.
- **Hazards** — large I/O, multiprocess + HDF5, GPU memory, long loops.

### 3) Promote parameters
Classify each literal / hardcoded value. When uncertain, expose via CLI.

| Category | Destination |
|---|---|
| Sweepable parameter | `argparse` argument |
| Path | `argparse` argument |
| True invariant | Module-level constant |
| Loop index / bookkeeping / intermediate | Local variable |

### 4) Restructure
Fit the extracted code into the `script-opinions` skeleton. The notebook's meat goes into `run_experiment(...)` with **minimal** edits — only change code to eliminate notebook-only constructs, remove reliance on globals, route outputs into the run dir, and expose hyperparameters via argparse. Leave ugly-but-correct scientific logic alone.

Any meaningful refactorings or code changes must be explicitly approved by the user/manager. Ask, if you are unsure. The goal is to preserve the original logic, exactly.

### 5) Headless conversion

| Notebook | Script |
|---|---|
| `print(...)` | `logger.info(...)` |
| `plt.show()` | `savefig(...)` + `close(fig)` (behind `--save-plots` if optional) |
| `display(df)` | `df.to_csv(filepath_out)` or `logger.info(df.to_string())` |
| inline cell outputs, magics | drop |

## Tools

Bundled Python helpers live in `scripts/` (e.g. `notebook_ingest.py`). Use them to convert `.ipynb` to script text before reasoning.
