# Specific parameters

## repository variables
- `<remote>`: True
- `<temp_data_dir>`: /n/netscratch/bsabatini_lab/Lab/rhakim/temp
- `<agent_assets_meta_directory>`: '/n/holylabs/kempner_rhakim_lab/Lab/rhakim/agent_assets/<repo>/'

Cluster/partition details: load `job-dispatch`.

## agent access
- Internet: True
- File editing: True
- Terminal: True

## Git rules
- commit: False
- push: False
- make PR: False

If the user asks for a specific git call, do it, then privileges reset to defaults.

## Compute
Activate `<conda_env_name>` before running code. Don't run compute on a login node — `ssh <compute_node_name>` first (it changes; recheck). For batch work load `job-dispatch`, which manages the worker/submitter pattern and (for SLURM) SBATCH templates, partition rules, and account selection.
