# Installing the Illustrator MCP

## Prerequisites

- macOS (uses osascript to communicate with Illustrator)
- Adobe Illustrator CC 2024+
- Node.js (for npx)

## Install

```bash
claude mcp add illustrator-mcp -- npx illustrator-mcp-server
```

This registers the MCP server with Claude Code. `npx` downloads and runs the package on demand — no global install needed.

## First run

On first use, macOS will prompt for automation permissions. Grant access in **System Settings > Privacy & Security > Automation**.

Illustrator must be running and a document must be open for most tools to work. If no document is open, use `create_document` or open one manually.

## Verify

```bash
claude mcp list
```

Should show `illustrator-mcp` as connected.

## Remove

```bash
claude mcp remove illustrator-mcp
```

## Alternative MCP servers

- **kevinschaul/illustrator-mcp-server** — 2 tools (screenshot + run arbitrary ExtendScript). Claude can see the canvas and self-correct. Good for iterative visual editing.
- **jinkeda/Illustrator_MCP** — 12 tools + 25 injectable libraries. Checkpoints, boolean ops, procedural generation, batch task protocol. Requires CEP panel install.
