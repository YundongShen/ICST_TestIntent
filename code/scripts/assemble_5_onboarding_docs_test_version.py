#!/usr/bin/env python3
"""Test version: validate saved case extractions and generate five onboarding documents."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from onboarding_test_utils import CASE_DIR, TEST_OUTPUT, case_id, document_case, generate_document, test_service, validate_record
from suites_data import SUITES


def load_cases(suite, directory=CASE_DIR):
    cases = []
    for index in range(1, len(suite["cases"]) + 1):
        identifier = case_id(suite, index)
        path = Path(directory) / f"{suite['suite_id']}_{identifier}.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("case_id") != identifier or record.get("suite_id") != suite["suite_id"]:
            raise ValueError("Case metadata does not match " + str(path))
        if record.get("validation", {}).get("passed") is not True:
            raise ValueError("Regenerate this case with the validated test-version extractor: " + str(path))
        cases.append(record)
    return cases


def assemble(suite, service, case_dir=CASE_DIR, output_dir=TEST_OUTPUT):
    records = load_cases(suite, case_dir)
    for record in records:
        validate_record(record, service)
    cases = [document_case(record) for record in records]
    safe_name = suite["suite_id"].lower().replace("-", "_")
    return generate_document(suite, cases, service,
                             Path(output_dir) / f"onboarding_{safe_name}_test_version.md")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", type=Path, default=CASE_DIR)
    parser.add_argument("--output-dir", type=Path, default=TEST_OUTPUT)
    args = parser.parse_args(argv)
    service = test_service()
    for suite in SUITES:
        print(assemble(suite, service, args.case_dir, args.output_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
