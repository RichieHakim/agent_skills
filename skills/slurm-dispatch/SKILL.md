---
name: slurm-dispatch
description: SLURM job submission infrastructure around an existing Python analysis script — worker .sh and Python batch submitter. Use when packaging a script for SLURM or running parameter sweeps via sbatch.
---

# SLURM Dispatch

Package an existing Python analysis script for SLURM. **Infrastructure only** — the worker shell script, the Python submitter, the directory layout. The analysis script itself must already conform to `script-opinions` (argparse, dual-handler logging, run dir). If it doesn't, fix it first via `notebook-to-script` or a direct refactor.

## Output layout

```text
<scripts_dir>/
├── <script_name>.py               # analysis script (argparse-based)
└── runs/
    ├── run_<script_name>.sh       # SLURM worker
    ├── submit_<script_name>.py    # Python batch submitter (stdlib-only)
    └── logs/                      # SLURM stdout/stderr
```

The submitter must import **only stdlib** so it runs under the base Python environment.

## Worker script (`run_<name>.sh`)

```bash
#!/bin/bash
#SBATCH --job-name=<short_name>
#SBATCH --account=<billing_account>
#SBATCH --partition=<partition>
#SBATCH --gres=gpu:<count>
#SBATCH --cpus-per-task=<cpus>
#SBATCH --mem=<memory>
#SBATCH --time=<time_limit>
#SBATCH --open-mode=append
#SBATCH --requeue

# $1 is ALWAYS the absolute path to the analysis script.
# $4 is ALWAYS --dir_save (the run directory; see script-opinions).
ANALYSIS_SCRIPT=$1
RUN_NAME=$2
ARG_A=$3
DIR_SAVE=$4
[ -z "$ANALYSIS_SCRIPT" ] || [ -z "$DIR_SAVE" ] && { echo "Usage: $0 <script> <run_name> <arg_a> <dir_save> ..."; exit 1; }
[ ! -f "$ANALYSIS_SCRIPT" ] && { echo "Error: $ANALYSIS_SCRIPT not found"; exit 1; }

PYTHON_EXEC="/path/to/.conda/envs/<env_name>/bin/python"
[ ! -x "$PYTHON_EXEC" ] && { echo "Error: $PYTHON_EXEC not executable"; exit 1; }

echo "Running $RUN_NAME (job=$SLURM_JOB_ID)"
$PYTHON_EXEC "$ANALYSIS_SCRIPT" \
    --arg-a "$ARG_A" \
    --dir_save "$DIR_SAVE"
RET=$?
exit $RET
```

## Submitter (`submit_<name>.py`)

Computes absolute paths, iterates datasets, calls `sbatch`.

```python
#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path
from typing import List, TypedDict

class DatasetSpec(TypedDict):
    name: str
    arg_a: str

DATASETS: List[DatasetSpec] = [
    {"name": "run_001", "arg_a": "/path/to/input_a"},
    # ...
]
OUTPUT_ROOT = "/path/to/output/root"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    worker = here / "run_<name>.sh"
    analysis = (here / "../<script_name>.py").resolve()
    logs = here / "logs"
    assert worker.exists() and analysis.exists()
    logs.mkdir(exist_ok=True)
    Path(OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)

    for i, d in enumerate(DATASETS):
        dir_save = str(Path(OUTPUT_ROOT) / d["name"])
        cmd = [
            "sbatch",
            f"--output={logs}/{d['name']}_%j.out",
            f"--error={logs}/{d['name']}_%j.err",
            str(worker),
            str(analysis),   # $1
            d["name"],       # $2
            d["arg_a"],      # $3
            dir_save,        # $4
        ]
        print(f"[{i+1}/{len(DATASETS)}] {' '.join(cmd)}")
        if not args.dry_run:
            subprocess.run(cmd, check=True, capture_output=True,
                           text=True, stdin=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
```

**Short throwaway sweeps:** skip the `TypedDict`; hardcode config at the top of the file and nest loops over your sweep axes (datasets × ranks × seeds, etc.). Use a stable `--job-name=<prefix>` so `scancel -n <prefix>` cancels the whole sweep at once. Worker stays unchanged.

## Rules (worker + submitter)

- **Absolute analysis-script path as `$1`.** The submitter computes it; the worker never resolves paths itself. Relative paths break in SLURM spool dirs.
- **Explicit `PYTHON_EXEC`.** Never `conda activate` in non-interactive bash.
- **All args required.** No defaults, no optionals, no env vars — fail loudly.
- **Propagate exit codes** (`exit $?`).
- **`stdin=subprocess.DEVNULL` + `capture_output=True` + `check=True`** on every `subprocess.run`. Prevents SLURM hangs; fails loudly.
- **No `try`/`except` around `subprocess.run`** that hides failures — let `CalledProcessError` propagate.
- **`TypedDict` for dataset specs**, not tuples.
- **Always support `--dry-run`** on the submitter.
- **No post-hoc log copying** — dual-handler logging from `script-opinions` already writes into `dir_save/logs/`.

## Array jobs (rc.fas.harvard.edu)

Scheduler caps active jobs at 16. For sweeps, prefer array jobs with `%15` (one slot free):

```bash
#SBATCH --array=0-99%15
```

Index `DATASETS[SLURM_ARRAY_TASK_ID]` in the worker or submitter.

## Pre-submit checklist

- Analysis script conforms to `script-opinions`.
- Worker reads the analysis-script path from `$1`; submitter computes and passes the absolute path.
- `runs/logs/` exists.
- Tested with `--dry-run` first.
