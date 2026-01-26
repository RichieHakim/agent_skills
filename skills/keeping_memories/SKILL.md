---
name: keeping_memories
description: How to maintain and update MEMORIES.md files for knowledge persistence
---

# Keeping Memories

MEMORIES.md files store domain knowledge and session logs that persist across agent sessions. Edit liberally - successful agents update this file at least once per prompt.

## Structure

```markdown
# MEMORIES.md - [Project/Feature Name]

## Abstract Context
Brief description of what this work accomplishes and why.

## Key Insights
The most important learnings that future agents need.

## Data Shapes / API Patterns
Technical details that are hard to rediscover.

## Session Log
Chronological record of what was tried and accomplished.

## Useful Paths
Frequently referenced directories and files.

## Tips for Future Agents
Actionable advice for common pitfalls and self-analysis of your own behavior.
```

## When to Update

- **After discovering non-obvious information** (data shapes, code patterns, API quirks)
- **After completing a task** (add to session log)
- **After hitting and resolving a blocker** (document the solution)
- **Whenever you think of something useful for future agents to know**

## Best Practices

1. **Be specific** - Include exact shapes, paths, and code snippets
2. **Date your entries** - Use session log format `## Session Log (YYYY-MM-DD)`
3. **Keep it scannable** - Use tables, code blocks, and bullet points
4. **Update the status table** - Track what's done vs pending
5. **Add tips as you learn them** - Future agents will thank you

## Location

- Create in `agent_assets/<feature_name>/MEMORIES.md`
- One per major feature or task
- Reference from other MEMORIES.md files if needed