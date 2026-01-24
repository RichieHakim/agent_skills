#!/usr/bin/env python3
"""Run the Nougat CLI to extract academic PDFs to Markdown."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Nougat on one or more PDFs and write Markdown outputs.",
    )
    parser.add_argument(
        "--pdf",
        nargs="+",
        required=True,
        help="PDF file(s) or a directory to process.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for Nougat results.",
    )
    parser.add_argument(
        "--model",
        help="Nougat model tag (e.g., 0.1.0-small).",
    )
    parser.add_argument(
        "--checkpoint",
        help="Path to a Nougat checkpoint directory.",
    )
    parser.add_argument(
        "--batchsize",
        type=int,
        help="Batch size for inference.",
    )
    parser.add_argument(
        "--pages",
        help="Page selection string like '1-4,7' (single PDF only).",
    )
    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="Disable Markdown postprocessing.",
    )
    parser.add_argument(
        "--no-skipping",
        action="store_true",
        help="Disable page skipping heuristic.",
    )
    parser.add_argument(
        "--full-precision",
        action="store_true",
        help="Use full precision (float32).",
    )
    parser.add_argument(
        "--recompute",
        action="store_true",
        help="Recompute results even if outputs exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the command and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if shutil.which("nougat") is None:
        print(
            "nougat CLI not found. Install with `pip install nougat-ocr` and ensure it is on PATH.",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["nougat"]
    cmd.extend(args.pdf)
    cmd.extend(["-o", str(out_dir)])

    if args.model:
        cmd.extend(["-m", args.model])
    if args.checkpoint:
        cmd.extend(["-c", args.checkpoint])
    if args.batchsize is not None:
        cmd.extend(["-b", str(args.batchsize)])
    if args.pages:
        cmd.extend(["-p", args.pages])
    if args.recompute:
        cmd.append("--recompute")
    if args.full_precision:
        cmd.append("--full-precision")
    if args.no_markdown:
        cmd.append("--no-markdown")
    if args.no_skipping:
        cmd.append("--no-skipping")

    if args.dry_run:
        print(" ".join(cmd))
        return 0

    subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
