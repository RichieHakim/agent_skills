#!/usr/bin/env python3
"""Run MinerU to extract PDF(s) to Markdown with a consistent output layout.

This script assumes a pre-existing conda environment named "mineru".
It does NOT install or modify environments; it only checks and reports.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract PDF(s) to Markdown using MinerU.",
    )
    parser.add_argument(
        "--filepath_pdf",
        required=True,
        help=(
            "Path to a single PDF file or a directory containing PDFs. "
            "If a directory is provided, MinerU will process all PDFs under it."
        ),
    )
    parser.add_argument(
        "--output_dir",
        required=True,
        help=(
            "Output directory where MinerU results will be written. "
            "Recommended: agent_assets/<project_name>/pdf_conversions."
        ),
    )
    parser.add_argument(
        "--method",
        choices=["auto", "txt", "ocr"],
        default="txt",
        help=(
            "Extraction method. 'txt' for digital PDFs with selectable text, "
            "'ocr' for scanned PDFs, 'auto' to let MinerU decide. Default: txt."
        ),
    )
    parser.add_argument(
        "--backend",
        default=None,
        help=(
            "Optional MinerU backend override (e.g., 'pipeline' for CPU-only). "
            "If omitted, MinerU uses its default hybrid backend."
        ),
    )
    parser.add_argument(
        "--preview-lines",
        type=int,
        default=0,
        help=(
            "If set (>0), print the first N lines of each extracted .md file "
            "to make it easy to pull into context."
        ),
    )
    return parser.parse_args()


def require_mineru_env() -> None:
    env = os.environ.get("CONDA_DEFAULT_ENV", "")
    if env != "mineru":
        msg = (
            "Expected conda env 'mineru'. Activate it with:\n"
            "  conda activate mineru\n"
            "Then re-run this script. If it does not exist, create it and install MinerU." 
        )
        print(msg, file=sys.stderr)
        raise SystemExit(2)

    if shutil.which("mineru") is None:
        print(
            "MinerU CLI not found on PATH in the 'mineru' env. "
            "Install MinerU in that env, then re-run.",
            file=sys.stderr,
        )
        raise SystemExit(3)


def find_md_files(out_dir: Path) -> list[Path]:
    return sorted(out_dir.rglob("*.md"))


def main() -> int:
    args = parse_args()
    require_mineru_env()

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["mineru", "-p", args.filepath_pdf, "-o", str(out_dir), "-m", args.method]
    if args.backend:
        cmd.extend(["-b", args.backend])

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    md_files = find_md_files(out_dir)
    if not md_files:
        print("No .md files found. Check MinerU logs/output.", file=sys.stderr)
        return 4

    print("Extracted Markdown files:")
    for md in md_files:
        print(f"- {md}")

    if args.preview_lines > 0:
        for md in md_files:
            print(f"\n--- {md} (first {args.preview_lines} lines) ---")
            try:
                with md.open("r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f):
                        if i >= args.preview_lines:
                            break
                        print(line.rstrip("\n"))
            except OSError as exc:
                print(f"Failed to read {md}: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
