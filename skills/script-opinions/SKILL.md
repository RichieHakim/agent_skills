---
name: script-opinions
description: Opinions for standalone Python scripts. Analysis runs, HPC jobs, batch processing.
---

# Script Opinions

Scripts must be **stateless, headless, reproducible, observable**. This extends the `coding-style` skill for standalone Python scripts.

Scripts should be:
- General: reusable across datasets and parameters. No hardcoded paths, magic numbers, or assumptions.
- Atomic: Do one thing well — when scope grows, note it and ask whether to extend or split. 
- Opinionated: Typed ingestion good; fallbacks and mode switches bad.

## Non-negotiables

These exist to make scripts debuggable on a cluster you don't control — they are infrastructure, not style.

1. **Top-to-bottom execution.** No hidden state, no `sys.path` hacks. Anchor imports to `__file__` or pip-install the repo.
2. **argparse** for all config. No Hydra, no env-var configs. (If the repo already uses a framework, match it and note the deviation.)
3. **stdlib `logging`** only. `logger.info`/`debug` not `print`. (Same: match existing frameworks if present.)
4. **Headless.** No `plt.show()`, `display()`, `input()`. Use headless backends.
5. **Run directory** per invocation with config snapshot, `logs/`, `artifacts/`.
6. **Fail fast.** Validate paths and assumptions before heavy work.
7. **Atomic writes.** Write to `<path>.tmp`, then `os.replace(tmp, path)`. For checkpoints and anything preemption could corrupt.
8. **Strict imports.** Loud `ImportError` at top level unless truly optional.
9. **No env vars** for config between script and submitter. Explicit args only.

## Standard skeleton

The skeleton is a floor, not a ceiling — instrument, annotate, and structure the core logic however best serves the script. Use `@dataclass` by default; `pydantic.BaseModel` only for runtime validation.

- `@dataclass ExperimentConfig` — typed, flat, hierarchical field names.
- `parse_args() -> ExperimentConfig` — argparse. Pull defaults from dataclass.
- `setup_dir_save(config) -> str` — creates `dir_save/{logs,artifacts,checkpoints}`.
- `setup_logging(dir_save, level)` — dual handlers: `FileHandler(logs/run.log)` + `StreamHandler(stdout)`. Both get the full log — no post-hoc copying from SLURM stdout.
- `set_determinism(seed, deterministic_torch=True)`, `save_config(dir_save, config)` (writes `.yaml` or `.json`).
- `run_experiment(config, logger)` — the scientific meat. Readable, flat. The design here is yours — bring judgment about what to measure, log, and save.
- `main()` wires: parse → dir → log → config → determinism → run.

## Run directory layout

```text
<dir_save>/
├── config.yaml        # parsed args snapshot
├── logs/run.log       # mirrored to stdout
├── artifacts/         # arrays, metrics, figures
└── checkpoints/       # optional; resumable state
```

## CLI arg names

`--dir_save`, `--name_run`, `--path_config`, `--path_data_*`, `--seed`, `--deterministic`, `--save-plots`, `--checkpoint-every-seconds`, `--resume`.

## Long-running jobs

- **Preemption safety:** `--checkpoint-every-{seconds,steps}` + `--resume`. Atomic writes. Validate checkpoint before new work.
- **Large I/O:** try to implement lazy loading, streaming, or chunking.
- **Multiprocess:** each worker opens its own file handle. Never share HDF5/zarr handles across processes.
- **Analysis plots:** save underlying arrays alongside figures for local regeneration.
