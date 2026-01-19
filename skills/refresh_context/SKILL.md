---
name: refresh_context
description: How to refresh context and understand a project quickly
---

# Refreshing Context

When starting work on an existing project or after a long gap, quickly orient yourself by reading key files in order.

## Steps

1. **Read `.agent/AGENTS.md`** - Contains project-specific parameters:
   - Conda environment name
   - Compute node access (SSH target, resources)
   - SBATCH templates
   - Special instructions

2. **Check `agent_assets/` directory** - Your personal knowledge store:
   - Find project-specific MEMORIES.md files
   - Check `code/` for utility scripts
   - Review any logs or test outputs

3. **Read relevant MEMORIES.md** - Contains:
   - Abstract context and key insights
   - Data shapes and access patterns
   - Session logs of what was tried/accomplished
   - Useful paths and tips

4. **Check conversation summary** (if available):
   - Review any checkpoint summaries
   - Note the current task status
   - Identify blocking issues

## Tips

- Don't skip AGENTS.md - it has critical environment info
- MEMORIES.md is your most valuable context source
- Look for `agent_assets/code/` scripts that may already solve your problem
- Check various `logs/` directories for recent run outputs
