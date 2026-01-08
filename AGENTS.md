# repository variables
- `conda_environment`: 'fr'
- `agent_assets` folder name: `agent_assets`
- `remote`: True
- `compute_node_name`: 'holygpu8a11204.rc.fas.harvard.edu'
- `compute_node_resources`: 'gpu:h100, cpu:24, mem:360G'

# agent access
- Internet: True
- Internet browsing: True
- File editing: True
- Terminal: True

# running code
- You are generally encouraged to run code. 
- You are encouraged to generate little scripts to run and test your code. Place them in `agent_assets/code`.
- After generating code, you are encouraged to try running and debugging on your own, unless there is a good reason to have the user in the loop.
- For running code, ensure that you are in the appropriate conda environment: `conda activate <conda_environment>`.
- If you are running on a remote node (see `remote` value), do not run compute intensive jobs on the login node. For running compute intensive jobs, ssh into `<compute_node>` first.

# artifact handling
- Look through your `agent_assets` directory, and always know what is in there. Use it as a quiver of tools and personal knowledge.
- Place any temporary code files (e.g. for checks) within the `agent_assets` folder in a subdirectory named `code`.
- If you come across an insightful piece of information, store it in a `MEMORIES.md` file within `agent_assets`
- Place all generated artifacts related to temporary/agentic work in the `agent_assets` folder.
- Be liberal in storing artifacts. Anything that you think will be helpful for guiding yourself in the future should be placed there.