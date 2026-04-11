---
name: script-opinions
description: Opinions for writing Python scripts that are stateless, headless, reproducible, and observable. Use when authoring or reviewing standalone Python scripts (analysis runs, HPC jobs, batch processing).
---

# Script Opinions

Scripts must be **stateless, headless, reproducible, observable**. This skill extends `coding-style` and applies to standalone Python scripts — analysis runs, HPC jobs, batch processing.

Scripts should be very general and resuable over different datasets and parameters. Options and parameters can be good in moderation. Hardcoding is bad. Opinionated ingestion is good. Fallbacks and different modes are very bad. 

Scripts should do atomic things well, not be Swiss Army knives. It's often good to ask if we should make a new script, instead.

## Non-negotiables

1. Runs top to bottom in a clean process. No hidden state, no `sys.path` hacks — anchor imports relative to `__file__` or make the repo pip-installable.
2. Use **argparse** for all user-facing config. No Hydra, no env-var configs.
3. **stdlib `logging`** only. No rich, no loguru. Replace `print` with `logger.info`/`debug`.
4. **Headless:** no `plt.show()`, `display()`, `input()`, or notebook magics. For plots: `matplotlib.use("Agg")` *before* pyplot, then `fig.savefig(...)` + `plt.close(fig)`.
5. **Run directory** per invocation (layout below) with a config snapshot, `logs/`, `artifacts/`.
6. **Fail fast.** Validate paths and critical assumptions *before* heavy loads or GPU work.
7. **Atomic writes** for important artifacts: write to `<path>.tmp` in the same directory (so the rename is atomic on POSIX), then `os.replace(tmp, path)`. Use for checkpoints, metrics snapshots, anything preemption could corrupt.
8. **Strict imports.** Raise `ImportError` loudly at the top-level imports block unless the dep is truly optional.
9. **No env vars** for passing config between a script and its submitter. Explicit argparse args only.

## Style

- **`pathlib.Path` for composition, `str` for storage.** Stringify at the boundary: `dir_run = str(Path(dir_save) / name_run)`. Don't hold `Path` in long-lived variables.
- **Naming:** long, hierarchical, type-first: `dir_*`, `filepath_*`, `kwargs_*`. Plurals for collections: `filepaths_models`.
- **Explicit keywords** in calls: `func(x=x, y=y)`.
- **Flat > clever.** Linear structure over nested abstractions.
- **Docstrings:** RST/Google-style with nested Returns blocks (see `coding-style`).

## Required skeleton

Every script must include these pieces (names may vary). Use `@dataclass` by default; switch to `pydantic.BaseModel` only if you need runtime validation.

- `@dataclass ExperimentConfig` — typed, flat, hierarchical field names.
- `parse_args() -> ExperimentConfig` — argparse. Pull defaults from the dataclass to avoid duplication: `default=ExperimentConfig.seed`.
- `setup_dir_save(config) -> str` — creates `dir_save/{logs,artifacts,checkpoints}`.
- `setup_logging(dir_save, level) -> logging.Logger` — **dual handlers**: `FileHandler(dir_save/logs/run.log)` + `StreamHandler(sys.stdout)`, shared formatter. SLURM's stdout *and* the results-adjacent file both get the full log — no post-hoc copying.
- `set_determinism(seed, deterministic_torch=True) -> None`.
- `save_config(dir_save, config) -> None` — writes `config.yaml` or `config.json` snapshot.
- `run_experiment(config, logger) -> None` — the scientific meat. Readable, flat.
- `main()` wires them in order: parse → dir → log → save_config → determinism → run.

## Run directory layout

```text
<dir_save>/
├── config.yaml        # snapshot of parsed args
├── logs/run.log       # FileHandler output, mirrored to stdout
├── artifacts/         # arrays, metrics, figures, tables
└── checkpoints/       # optional; resumable state
```

## Conventional CLI arg names

`--dir_save`, `--name_run`, `--path_config` (`.json`/`.yaml`), `--path_data_*`, `--seed`, `--deterministic`, `--save-plots`, `--checkpoint-every-seconds`, `--resume`.

## Long-running / large jobs

- **Preemption safety:** `--checkpoint-every-{seconds,steps}`, `--resume` loads the latest checkpoint, atomic writes, validate/load cleanly before new work.
- **Large I/O:** stream/chunk from HDF5, memmap, or zarr. Don't load massive arrays fully unless required.
- **Multiprocess dataloaders:** each worker opens its *own* file handle. Never share an HDF5/zarr handle across processes.
- **Analysis plots:** save the underlying arrays/tables alongside, so plots can be regenerated locally without rerunning the job.
