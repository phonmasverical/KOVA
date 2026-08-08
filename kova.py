#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOVA — code. create. evolve.

CLI entry point for the KOVA programming language interpreter.

Usage:
    python kova.py                  Launch interactive REPL
    python kova.py <file.kv>        Run a .kv source file
    python kova.py --version        Show version information
    python kova.py --help           Show help

Author : Nguyen Khoi
Version: 1.0.0
License: MIT
"""

import sys
import os

# Ensure the directory containing this script is on the path so kova_core can
# be imported regardless of where the user invokes the command from.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from kova_core import (
    KOVA_VERSION,
    KOVA_AUTHOR,
    run_file,
    run_repl,
)

HELP_TEXT = f"""\
KOVA Programming Language v{KOVA_VERSION}
Author: {KOVA_AUTHOR}

Usage:
  python kova.py                  Launch the interactive REPL
  python kova.py <file.kv>        Execute a KOVA source file
  python kova.py --version, -v    Print version and exit
  python kova.py --help, -h       Show this help message

File extension: .kv

Examples:
  python kova.py hello.kv         Run hello.kv
  python kova.py                  Start REPL session

For language documentation, see the examples/ directory.
"""


def main() -> None:
    """CLI entry point."""
    args = sys.argv[1:]

    if not args:
        # No arguments — launch REPL
        run_repl()
        return

    first = args[0]

    if first in ("--help", "-h"):
        print(HELP_TEXT)
        return

    if first in ("--version", "-v"):
        print(f"KOVA v{KOVA_VERSION}")
        return

    # Treat the first argument as a file path
    filepath = first
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    run_file(filepath)


if __name__ == "__main__":
    main()
