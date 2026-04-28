# agent_skills

A collection of agent skills for scientific and software engineering work.

## Install

Symlink each skill into both Claude Code and Codex:

```bash
./sync_skills.sh
```

The script links every directory in `skills/` into:

- `~/.claude/skills/`
- `~/.codex/skills/`

The repo remains the source of truth. Editing a skill here updates both agents automatically because the installed skills are symlinks. Run the script again after adding, renaming, or removing skills.
