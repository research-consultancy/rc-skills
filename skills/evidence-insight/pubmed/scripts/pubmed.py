#!/usr/bin/env python3
"""Portable entry point for the bundled PubMed agent tool."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pubmed_tool.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
