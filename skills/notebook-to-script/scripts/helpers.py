
#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Sequence

import nbformat


def comment_line(line: str) -> str:
    """
    Comments out a line, preserving indentation when possible.

    Args:
        line (str):
            A single line of code.

    Returns:
        (str):
            commented (str):
                Commented line.
    """
    match_indent = re.match(r"^(\s*)(.*)$", line)
    if not match_indent:
        return "# " + line
    indent, rest = match_indent.group(1), match_indent.group(2)
    if rest.strip() == "":
        return line
    if rest.lstrip().startswith("#"):
        return line
    return f"{indent}# {rest}"


def notebook_to_script_text(
    notebook_path: Path,
    cell_types: Sequence[str] = ("code", "markdown"),
) -> str:
    """
    Converts a notebook into a script-like text. Markdown is included as comments.

    Notes:
    - This is intended for *ingestion into an agent's context*, not as the final
      HPC script.

    Args:
        notebook_path (Path):
            Path to the input .ipynb file.
        cell_types (Sequence[str]):
            Cell types to include. Typically includes "code" and optionally "markdown".

    Returns:
        (str):
            script_text (str):
                Script text assembled from notebook cells.
    """
    nb = nbformat.read(str(notebook_path), as_version=4)

    chunks: List[str] = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type not in cell_types:
            continue

        chunks.append(f"\n# -------------------- cell {idx:03d} ({cell.cell_type}) --------------------\n")

        if cell.cell_type in ("markdown", "raw"):
            md_lines = cell.source.splitlines()
            for line in md_lines:
                chunks.append("# " + line + "\n")
            chunks.append("\n")
            continue

        if cell.cell_type == "code":
            chunks.append(cell.source + "\n")

    return "".join(chunks).rstrip()
