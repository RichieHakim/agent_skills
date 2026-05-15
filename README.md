# agent_skills

A collection of agent skills for scientific and software engineering work.

## Install

Symlink each skill into the default Claude Code and Codex skill directories:

```bash
./sync_skills.sh
```

The script links every directory in `skills/` into:

- `~/.claude/skills/`
- `~/.codex/skills/`

To override the targets, pass directories explicitly:

```bash
./sync_skills.sh /path/to/agent/skills [/path/to/other/agent/skills]
```

Or use a colon-separated environment variable:

```bash
AGENT_SKILL_DIRS="/path/to/agent/skills:/path/to/other/agent/skills" ./sync_skills.sh
```

The repo remains the source of truth. Editing a skill here updates configured agents automatically because the installed skills are symlinks. Run the script again after adding, renaming, or removing skills.
