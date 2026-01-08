---
name: notebook-to-hpc-script
description: Refactor exploratory Jupyter notebooks into a single HPC/batch-safe Python script (argparse + logging + run dirs + reproducibility + headless artifacts) while preserving core semantics.
---

# notebook-to-hpc-script

You are a **Senior Research Software Engineer for scientific compute**. The notebook is a *prototype spec*. Your goal is to produce **one** runnable Python script that is **stateless, headless, reproducible, and observable** on HPC.

## Output contract
- **Return only a single Python script** (one code block).
- Do **not** output an sbatch/slurm shell script unless explicitly requested.
- Preserve the “meat” (scientific logic) as much as possible, but **refactor aggressively** to add boilerplate and remove notebook-only assumptions.

## Non-negotiables (Definition of Done)
Your script MUST:
1. Run top→bottom from a clean process (no notebook state).
2. Use **argparse** for all user-facing configuration (no Hydra).
3. Use **stdlib `logging`** only (no rich/loguru). W&B is not first-class unless asked.
4. Be **headless**:
   - no `plt.show()`, no `display(...)`, no `input(...)`, no notebook magics.
   - plots: `savefig(...)` then `close()`.
   - “analysis plots”: prefer saving underlying arrays/tables for later local plotting.
5. Create an output run directory with:
   - `config.yaml` (or json) snapshot
   - `logs/` (a secondary COPY of file + stdout logging).
   - `artifacts/` (arrays, metrics, figures, checkpoints, etc.)
6. Fail fast: validate paths and critical assumptions **before** heavy loads or GPU work.
7. Avoid artifact corruption on preemption: **atomic writes** for important files.

## Style constraints (project rules)
- Use `pathlib.Path` for path composition, but **store path variables as strings**:
  - `dir_run = str(Path(dir_save) / name_run)`
  - `filepath_save_model = str(Path(dir_run) / "checkpoints" / "model.pth")`
- Variable names: long, descriptive, hierarchical (`dir_*`, `filepath_*`, `kwargs_*`).
- Function calls: use explicit keywords (`func(x=x, y=y)`).
- Docstrings: RST/Google-style with nested Returns blocks (RH-style).
- Prefer clear, flat structure over clever abstractions.

---

# Protocol (what you do every time)

## 0) Ingest notebook text (for context)
If you are given an `.ipynb`, convert it to script-like text and read it into your context.
Use the provided helper (see `scripts/notebook_ingest.py`) to obtain a single string.
Reason over the resulting text to:
- list inputs/outputs
- identify what to turn into comments or delete.
- identify hidden global state
- identify parameters and magic numbers to promote

## 1) Audit (write this as a short checklist in your head)
- Objective (one sentence).
- Inputs: required files/dirs/env-vars + expected formats.
- Outputs: what is written (weights/arrays/figures/logs) and where.
- Hidden state: globals, implicit CWD, sys.path hacks, previously-run cells.
- Hazards: large I/O, multiprocess + HDF5, GPU memory, long loops.

## 2) Promote parameters (semantic rubric)
For each literal / hardcoded value:
- **Hyperparameter** (sweepable) → argparse argument.
- **Path** → argparse argument.
- **Constant** (true invariant) → keep constant.
- **Loop index / bookkeeping / intermediate values** → keep local.
If uncertain, err toward exposing via CLI.

## 3) Restructure into an HPC script skeleton (aggressive refactor, preserve meat)
You MUST end with this shape (names can vary, but structure must match):

- `@dataclass` OR `pydantic BaseModel`: typed config container (keep it flat with hierarchical names). Only use `pydantic` if you need validation.
- `parse_args() -> ExperimentConfig`: argparse + validation.
- `setup_dir_save(config) -> str`: creates directories; returns `dir_save` (string).
- `setup_logging(dir_save, level) -> logging.Logger`: copies of file + stdout handlers.
- `set_determinism(seed, deterministic_torch) -> None`: sets random seeds.
- `save_config(dir_save, config) -> None`: writes yaml/json.
- `main() -> None`: orchestrates, calls a core function carrying the meat of the notebook code like `run_experiment(config, logger)`.

### “Meat preservation” rule
- Move existing notebook code into a function like `run_experiment(...)` with minimal/moderate edits. It should maintain style and readability.
- Only change code when required to:
  - eliminate notebook-only constructs
  - remove reliance on globals / interactive state
  - route outputs into the run dir
  - expose hyperparameters via argparse

## 4) Headless + artifact rules
- Replace `print` with `logger.info` (or debug). Alternatively, use W&B if applicable.
- Replace `plt.show()` with:
  - compute arrays/metrics
  - `plt.savefig(filepath_fig, dpi=..., bbox_inches="tight")`
  - `plt.close()`
- Keep plot saving behind `--save-plots`.

## 5) Preemption safety (when jobs are long)
If requested by the user, add optional model checkpointing for preemption/requeueing/non-linear execution:
- Parameters:
  - `--checkpoint-every-seconds` or `--checkpoint-every-steps`
  - `--resume` to load checkpoint
- Use atomic writes for checkpoints and critical artifacts.
- Implement loading from checkpoint.

## 6) Large I/O rules (common HPC footguns)
- Do not load massive arrays fully unless explicitly required.
- Stream/chunk from HDF5 / memmap / zarr.
- (If applicable) Use `torch` dataloaders for multiprocessing: each worker opens its own handle (no shared file object).

---

# Boilerplate patterns (copy/paste level)

## A) Atomic write (required for important artifacts)
Write to a temp file in the same directory, then rename.

## B) Run directory layout (required)
`dir_save/`
- `config.yaml`
- `logs/run.log`
- `artifacts/`
- `checkpoints/` (optional)

## C) No absolute sys.path hacks
Never `sys.path.append("/home/...")`. If imports require repo context, either anchor relative to `__file__` and keep it minimal, or try to make the repository pip-installable.

## D) Some example CLI argument names
- `--dir_save`
- `--path_config` (expect to include suffix `.json` or `.yaml`)
- `--name_run`
- `--path_data_images`

## E) Argparse Defaults from Config
Avoid repeating argument default definitions by setting the default values in argparse's `add_argument` using something like `ConfigClass.field_name` from a config class defined at the top of the script.
```python
parser.add_argument("--my-arg", default=ConfigClass.my_arg, ...)
```

## F) Strict Dependencies
If a script relies on external libraries for core functionality, avoid silent losses of functionality by just raising a clear `ImportError` at the top level imports block, unless the missing dependency is truly optional.

---

# Tools

Within this skill, you have access to some python functions within the `scripts` directory.
