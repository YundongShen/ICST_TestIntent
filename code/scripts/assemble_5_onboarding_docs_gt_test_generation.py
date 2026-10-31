#!/usr/bin/env python3
"""Test generation version: build five onboarding documents from the reviewed GT files."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from onboarding_test_utils import TEST_OUTPUT, default_groundtruth_dir, generate_document, load_groundtruth_cases, test_service
from suites_data import SUITES


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--groundtruth-dir", type=Path, default=default_groundtruth_dir(),
                        help="Path to ICST_TestIntent/Data/Groundtruth, or set GROUNDTRUTH_DIR")
    parser.add_argument("--output-dir", type=Path, default=TEST_OUTPUT)
    args = parser.parse_args(argv)

    prepared = [(suite, load_groundtruth_cases(suite, args.groundtruth_dir)) for suite in SUITES]
    service = test_service()
    for suite, cases in prepared:
        safe_name = suite["suite_id"].lower().replace("-", "_")
        target = Path(args.output_dir) / f"onboarding_{safe_name}_groundtruth_test_generation.md"
        print(generate_document(suite, cases, service, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
