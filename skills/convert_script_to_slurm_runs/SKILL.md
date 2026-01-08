# Convert Python Script to SLURM Runs

**Purpose**  
This skill provides a guide for creating SLURM job submission infrastructure around an existing Python analysis script. It produces a standardized directory structure with a worker `.sh` script and a Python batch submission script.

---

## Output Structure

```
<scripts_dir>/
├── <script_name>.py          # The main analysis script (argparse-based)
└── runs/
    ├── run_<script_name>.sh      # SLURM worker script
    ├── submit_<script_name>.py   # Python batch submission script
    └── logs/                     # SLURM output/error logs
```

---

## Requirements for the Analysis Script

The Python script must:
1. Use `argparse` for configuration
2. Accept `--dir_save` (output directory where results and logs are saved)
3. **Use Python stdlib `logging` with dual handlers** (see Logging Pattern below)
4. Be executable as: `python script.py --arg1 val1 --arg2 val2 ...`

---

## Logging Pattern (Critical)

The Python script must implement dual logging using stdlib `logging`:

```python
import logging
import sys
from pathlib import Path


def setup_logging(dir_run: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up logging to both stdout and file.
    
    This ensures logs are:
    1. Captured by SLURM in runs/logs/ (via stdout)
    2. Saved directly to dir_save/logs/ (via FileHandler)
    """
    logger = logging.getLogger("<script_name>")
    logger.setLevel(level)
    logger.handlers = []  # Clear any existing handlers

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # FileHandler: writes to dir_save/logs/run.log
    fh = logging.FileHandler(str(Path(dir_run) / "logs" / "run.log"))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # StreamHandler: writes to stdout (captured by SLURM)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger
```

**Why this pattern?**
- SLURM captures stdout/stderr to `runs/logs/`, but these logs are far from the output data
- The FileHandler writes directly to `dir_save/logs/run.log`, keeping logs with results
- Both logs contain identical content, no post-hoc copying needed

---

## SLURM Worker Script (`run_<name>.sh`)

### Template Structure

```bash
#!/bin/bash
#
# SLURM worker script for running <analysis_name>.
# Called by submit_<name>.py with explicit arguments.
#

#SBATCH --job-name=<short_name>
#SBATCH --account=<billing_account>
#SBATCH --partition=<partition>
#SBATCH --gres=gpu:<count>
#SBATCH --cpus-per-task=<cpus>
#SBATCH --mem=<memory>
#SBATCH --time=<time_limit>
#SBATCH --open-mode=append
#SBATCH --requeue

# -----------------------------------------------------------------------------
# Arguments (all required, passed from submit script)
# -----------------------------------------------------------------------------
RUN_NAME=$1
ARG_A=$2
ARG_B=$3
# ... more args

# Validate required arguments
if [ -z "$RUN_NAME" ] || [ -z "$ARG_A" ] || [ -z "$ARG_B" ]; then
    echo "Usage: $0 <run_name> <arg_a> <arg_b> ..."
    exit 1
fi

# -----------------------------------------------------------------------------
# Environment Setup
# -----------------------------------------------------------------------------
# Use explicit python executable from conda environment.
# This avoids issues with conda activation in non-interactive shells.
CONDA_ENV="<env_name>"
PYTHON_EXEC="/path/to/.conda/envs/${CONDA_ENV}/bin/python"

# Verify python executable exists
if [ ! -x "$PYTHON_EXEC" ]; then
    echo "Error: Python executable not found at $PYTHON_EXEC"
    exit 1
fi

# -----------------------------------------------------------------------------
# Path Resolution
# -----------------------------------------------------------------------------
# Get directory containing this script using BASH_SOURCE.
# BASH_SOURCE[0] is the path to this script, even when sourced.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Analysis script is one level up from runs/
ANALYSIS_SCRIPT="${SCRIPT_DIR}/../<script_name>.py"

if [ ! -f "$ANALYSIS_SCRIPT" ]; then
    echo "Error: Analysis script not found at $ANALYSIS_SCRIPT"
    exit 1
fi

# -----------------------------------------------------------------------------
# Run Analysis
# -----------------------------------------------------------------------------
echo "Running analysis: $RUN_NAME"

$PYTHON_EXEC "$ANALYSIS_SCRIPT" \
    --arg-a "$ARG_A" \
    --arg-b "$ARG_B"

exit $?
```

### Key Patterns

1. **Explicit Python Path**: Use full path to conda python, not `conda activate`
2. **BASH_SOURCE**: Use for reliable script directory resolution
3. **All Arguments Required**: No optional arguments; fail loudly if missing
4. **No Post-Hoc Log Copying**: Python script handles its own file logging

---

## Python Submission Script (`submit_<name>.py`)

### Template Structure

```python
#!/usr/bin/env python3
"""
Submit <analysis_name> jobs for multiple datasets via SLURM.

Usage:
    python submit_<name>.py --dry-run
    python submit_<name>.py
"""

import argparse
import subprocess
from pathlib import Path
from typing import List, TypedDict


# -----------------------------------------------------------------------------
# Dataset Definitions
# -----------------------------------------------------------------------------
# Use TypedDict for explicit, typed dataset specifications.
# All fields are required; no optional/None values.

class DatasetSpec(TypedDict):
    """Type definition for dataset specifications."""
    name: str           # Unique run identifier (used in output dir and logs)
    arg_a: str          # First required argument
    arg_b: str          # Second required argument


DATASETS: List[DatasetSpec] = [
    {
        "name": "descriptive_run_name_001",
        "arg_a": "/path/to/input_a",
        "arg_b": "/path/to/input_b",
    },
    # Add more datasets...
]

OUTPUT_ROOT = "/path/to/output/root"


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Submit jobs to SLURM.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    current_dir = Path(__file__).resolve().parent
    worker_script = current_dir / "run_<name>.sh"
    logs_dir = current_dir / "logs"
    
    assert worker_script.exists(), f"Worker script not found: {worker_script}"
    
    logs_dir.mkdir(exist_ok=True)
    Path(OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)
    
    for i, dataset in enumerate(DATASETS):
        run_name = dataset["name"]
        dir_save = str(Path(OUTPUT_ROOT) / run_name)
        
        cmd = [
            "sbatch",
            f"--output={logs_dir}/<name>_{run_name}_%j.out",
            f"--error={logs_dir}/<name>_{run_name}_%j.err",
            str(worker_script),
            run_name,
            dataset["arg_a"],
            dir_save,
            dataset["arg_b"],
        ]
        
        print(f"[{i+1}/{len(DATASETS)}] {run_name}")
        print(f"  Command: {' '.join(cmd)}")
        
        if not args.dry_run:
            subprocess.run(cmd, check=True)
            print("  Submitted.")
        else:
            print("  (dry-run)")


if __name__ == "__main__":
    main()
```

### Key Patterns

1. **TypedDict**: Use for explicit, typed dataset specs
2. **No Optional Fields**: All dataset fields required; fail loudly if missing
3. **Run Name**: Each dataset has a `name` used for output dir and log naming
4. **Dry-Run**: Always support `--dry-run` for testing

---

## Checklist

- [ ] Create `runs/` directory with `logs/` subdirectory
- [ ] Create `.sh` worker script with explicit python path
- [ ] Create `.py` submit script with TypedDict datasets
- [ ] Implement `setup_logging()` in the analysis script with dual handlers
- [ ] Ensure all arguments are explicitly required (no optional/None)
- [ ] Test with `--dry-run` before actual submission

---

## Anti-Patterns to Avoid

1. **Don't use `conda activate`** in non-interactive bash scripts
2. **Don't use optional arguments** or `if arg is not None` patterns
3. **Don't use tuples** for dataset specs; use dicts with descriptive keys
4. **Don't swallow errors** with try/except in the worker script
5. **Don't copy logs post-hoc** from shell; use Python logging with dual handlers
