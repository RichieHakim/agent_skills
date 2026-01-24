# Specific parameters
## repository variables
- <conda_environment>: '/n/holylabs/bsabatini_lab/Users/rhakim/envs/afm'
- <agent_assets> folder name: `agent_assets/`
- <remote>: True
- <compute_node_name>: 'holygpu8a13402.rc.fas.harvard.edu'
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
- For running code, ensure that you are on the compute node using `ssh <compute_node_name>` in the appropriate conda environment: `conda activate <conda_environment>`. Do not run code on the login node.
- It is wise to always check what the current compute node is before starting new jobs as it may have changed since the last time you checked.
- If you are running on a remote node (see `remote` value), do not run compute intensive jobs on the login node. For running compute intensive jobs, ssh into `<compute_node>` first.

## submitting jobs with custom resources
- You may look up available resources using `sinfo` and `squeue`.
- You may request from the following available GPU options by selecting the appropriate `--partition` flag:
  - `kempner`: GPU - A100; always use -c 16 --mem=250G
  - `kempner_h100`: GPU - H100; always use -c 24 --mem=375G
- Unless explicitly asked, do not select other partitions or resource configurations.
- The slurm scheduler on rc.fas.harvard.edu constrains the number of active jobs to be 16. It is wise to use array jobs with %15 to allow for a free slot for other jobs to run in.

## artifact handling
- Make and use an <agent_assets> directory that is in the repo top-level, and make a task/project specific subdirectory within it. Always know what is in there. It is your personal quiver of tools and knowledge.
- Make and use a `code/` directory within the task/project specific subdirectory of <agent_assets>. Place any temporary code files (e.g. for checks) within it.
- Use a `MEMORIES.md` file within the task/project specific subdirectory of <agent_assets> to store knowledge liberally; the most successful agents typically reference and edit this file at least once per prompt to describe specific knowledge, insights, and a log of what has been tried and accomplished.
- Place all generated artifacts related to temporary/agentic work in the task/project specific subdirectory of <agent_assets>.
- Be liberal in storing artifacts. _Anything_ that you think will be helpful for guiding yourself in the future should be placed there.

```
agent_assets/
└── <task_name>/      # task/project specific subdirectory
    ├── MEMORIES.md       # Knowledge base for ablation work
    └── code/         # Feature-specific temporary code
```

## skills
Skills are located in `.agent/skills/`. Each skill folder contains a `SKILL.md` with instructions. View the SKILL.md before using a skill.

| Skill | Purpose |
|-------|---------|
| `refresh_context` | How to refresh context and understand a project quickly |
| `keeping_memories` | How to maintain and update MEMORIES.md files |
| `convert_scientific_notebook_to_script` | Convert Jupyter notebooks to standalone scripts |
| `convert_script_to_slurm_runs` | Create SLURM submission scripts from Python code |
| `coding_style` | Coding conventions for this project |