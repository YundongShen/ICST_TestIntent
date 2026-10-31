#!/usr/bin/env python3
"""Alternate entry point for the case-level dataset extraction runner.

Use the same arguments as run_dataset.py. The selected processing stage and
extraction attempts are recorded by that runner.
"""

from run_dataset import main


if __name__ == "__main__":
    raise SystemExit(main())

