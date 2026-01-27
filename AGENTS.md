# Specific parameters
## repository variables
- <remote>: True
- <conda_env_name>: 'wm'
- <compute_node_name>: 'holygpu8a15603.rc.fas.harvard.edu'
- <compute_node_resources>: 'gpu:h100, cpu:24, mem:360G'
- <temp_data_dir>: /n/netscratch/bsabatini_lab/Lab/rhakim/temp
- <account_name>: 'kempner_rhakim_lab'

## agent access
- Internet: True
- Internet browsing: True
- File editing: True
- Terminal: True

## SBATCH template
```bash
#SBATCH --account=<account_name>
#SBATCH --time=0-48:00:00
#SBATCH --partition=kempner
#SBATCH --gres=gpu:1 
#SBATCH -c 16
#SBATCH --mem=250G
```

# General Instructions
## running code
- You are encouraged to run code.
- After generating code, you are encouraged to try running and debugging on your own.
- For running code, ensure that you are on the compute node using `ssh <compute_node_name>` in the appropriate conda environment: `conda activate <conda_env_name>`. Do not run code on the login node.
- It is wise to always check what the current compute node is before starting new jobs as it may have changed since the last time you checked.
- If you are running on a remote node (see `remote` value), do not run compute intensive jobs on the login node. For running compute intensive jobs, ssh into `<compute_node>` first.

## submitting jobs with custom resources
- You may look up available resources using `sinfo` and `squeue`.
- You may request from the following available GPU options by selecting the appropriate `--partition` flag:
  - `kempner`: GPU - A100; always use -c 16 --mem=250G
  - `kempner_h100`: GPU - H100; always use -c 24 --mem=375G
- Unless explicitly asked, do not select other partitions or resource configurations.
- The slurm scheduler on rc.fas.harvard.edu constrains the number of active jobs to be 16. It is wise to use array jobs with %15 to allow for a free slot for other jobs to run in.
