---
name: job-dispatch
description: Job dispatch infrastructure. Use when packaging a python script for batch / parallel execution, locally or on SLURM.
---

# Job Dispatch

Package an existing Python core/analysis script for batch execution. This skill handles **infrastructure only** — the worker shell script, the Python submitter, the directory layout. The same worker `.sh` and submitter run can run locally or on SLURM by switching is a one-line change in the submitter. The core script itself must already conform to `script-opinions` (argparse, dual-handler logging, run dir). If it doesn't, fix it first.

## Output layout

```text
<scripts_dir>/
├── <script_name>.py               # analysis script (argparse-based)
└── runs/
    ├── run_<script_name>.sh       # worker (one file, both backends)
    ├── submit_<script_name>.py    # Python submitter (stdlib-only)
    └── logs/                      # stdout/stderr
```

The submitter must import **only stdlib** so it runs under the base Python environment.

## Worker script (`run_<name>.sh`)

One worker file works for both backends. The `#SBATCH` header is inert under local dispatch — those lines are bash comments to any non-`sbatch` invocation. For SLURM, fill in account, partition, and resources — see `references.md` for ready-to-paste templates.

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

echo "Running $RUN_NAME (job=${SLURM_JOB_ID:-local})"
$PYTHON_EXEC "$ANALYSIS_SCRIPT" \
    --arg-a "$ARG_A" \
    --dir_save "$DIR_SAVE"
RET=$?
exit $RET
```

## Submitter (`submit_<name>.py`)

Backend is a module-level constant — a wrong-backend flip should be a one-line diff in a review, not an invisible argv. Dispatch logic is isolated in named helpers so the main loop reads backend-agnostic; the two helpers are the *only* places backend-specific argv lives.

```python
#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path
from typing import Callable, TypedDict

BACKEND: str = "slurm"   # "local" or "slurm"

class DatasetSpec(TypedDict):
    name: str
    arg_a: str

DATASETS: list[DatasetSpec] = [
    {"name": "run_001", "arg_a": "/path/to/input_a"},
    # ...
]
OUTPUT_ROOT = "/path/to/output/root"

def dispatch_local(worker: Path, worker_args: list[str], _name: str, _logs: Path) -> list[str]:
    return ["bash", str(worker), *worker_args]

def dispatch_slurm(worker: Path, worker_args: list[str], name: str, logs: Path) -> list[str]:
    return [
        "sbatch",
        f"--output={logs}/{name}_%j.out",
        f"--error={logs}/{name}_%j.err",
        str(worker), *worker_args,
    ]

DISPATCH: dict[str, Callable[[Path, list[str], str, Path], list[str]]] = {
    "local": dispatch_local,
    "slurm": dispatch_slurm,
}

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

    build_cmd = DISPATCH[BACKEND]
    for i, d in enumerate(DATASETS):
        dir_save = str(Path(OUTPUT_ROOT) / d["name"])
        worker_args = [str(analysis), d["name"], d["arg_a"], dir_save]
        cmd = build_cmd(worker, worker_args, d["name"], logs)
        print(f"[{i+1}/{len(DATASETS)}] {' '.join(cmd)}")
        if not args.dry_run:
            subprocess.run(cmd, check=True, capture_output=True,
                           text=True, stdin=subprocess.DEVNULL)

if __name__ == "__main__":
    main()
```

**Short throwaway sweeps:** skip the `TypedDict`; hardcode config at the top of the file and nest loops over your sweep axes. Worker stays unchanged.

## Rules (shared)

- **Absolute analysis-script path as `$1`.** Submitter computes it; worker never resolves paths. Relative paths break in SLURM spool dirs.
- **Explicit `PYTHON_EXEC`.** Never `conda activate` in non-interactive bash.
- **All args required.** No defaults, no optionals, no env vars — fail loudly.
- **Propagate exit codes** (`exit $?`).
- **`stdin=subprocess.DEVNULL` + `capture_output=True` + `check=True`** on every `subprocess.run`. Prevents SLURM hangs; fails loudly.
- **No `try`/`except` around `subprocess.run`** that hides failures — let `CalledProcessError` propagate.
- **`TypedDict` for dataset specs**, not tuples.
- **Always support `--dry-run`** on the submitter.

## Backend matrix

| Concern            | Local                                   | SLURM                                       |
|---                 |---                                      |---                                          |
| `#SBATCH` header   | Inert (bash comments)                   | Active; fill account/partition/gres         |
| Cancel-all         | `pkill -f run_<name>.sh`                | `scancel -n <job-name>`                     |
| Use when           | Short, I/O-bound, local has appropriate compute resources, smoke tests | Long, GPU-bound, resource-isolated, sweeps  |

## Backend: Local
*Applies only when `BACKEND = "local"`.*

- Sequential by default. For fan-out, wrap the main loop in `concurrent.futures.ProcessPoolExecutor`.
- `check=True` stops the loop at the first failure — intentional; you're usually debugging or smoke-testing.
- `ctrl-C` under a pool is flaky. Keep `pkill -f run_<name>.sh` ready.

## Backend: SLURM
*Applies only when `BACKEND = "slurm"`.*

- Fill the `#SBATCH` account + partition + resources from `references.md`. The combo must be valid on the target cluster.
- Use a stable `--job-name=<prefix>` so `scancel -n <prefix>` cancels the whole sweep at once.
- **Array jobs for big sweeps.** For ~20+ jobs, array jobs are easier to manage than looping `sbatch`. Array mode needs a different worker/submitter shape than the base pattern above: the submitter writes a lookup table (one row per dataset) and submits a single array job, and the worker reads `$SLURM_ARRAY_TASK_ID` to pick its row. The throttle `%N` caps concurrent tasks (e.g., `--array=0-99%15`) — check `references.md` for per-account caps before setting it.

## Pre-submit checklist

**Both backends:**
- Analysis script conforms to `script-opinions`.
- `BACKEND` constant set to the intended target.
- `runs/logs/` exists.
- Tested with `--dry-run` first.

**SLURM only:**
- `#SBATCH` header uses an account + partition combination valid on the target cluster (see `references.md`).

## References

- `references.md` — Cluster cheat sheet: partitions, billing accounts, fairshare guidance, ready-to-paste `#SBATCH` blocks per partition, scheduler caps. Consult before filling in the worker's `#SBATCH` header.
