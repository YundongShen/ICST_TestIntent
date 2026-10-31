#!/usr/bin/env python3
"""Test version: extract, validate, and adjust one case for onboarding."""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from onboarding_test_utils import CASE_DIR, case_id, extract_validate_adjust, test_service
from suites_data import SUITES, isolate_case_source


def flatten_tasks():
    return [(suite, case_id(suite, index), title, body)
            for suite in SUITES
            for index, (title, body) in enumerate(suite["cases"], 1)]


def run_task(index, service, output_dir=CASE_DIR, max_reextract=2):
    tasks = flatten_tasks()
    if not 0 <= index < len(tasks):
        raise ValueError(f"task-index must be between 0 and {len(tasks) - 1}")
    suite, identifier, title, body = tasks[index]
    source = isolate_case_source(suite, title, body)
    result = extract_validate_adjust(source, service, max_reextract=max_reextract)
    record = {
        **result, "version": "test", "suite_id": suite["suite_id"], "case_id": identifier,
        "title": title, "source_file": suite["source_file"], "dependencies": suite["dependencies"],
    }
    target = Path(output_dir) / f"{suite['suite_id']}_{identifier}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-index", type=int, required=True, choices=range(len(flatten_tasks())))
    parser.add_argument("--output-dir", type=Path, default=CASE_DIR)
    parser.add_argument("--max-reextract", type=int, default=2)
    args = parser.parse_args(argv)
    target = run_task(args.task_index, test_service(), args.output_dir, args.max_reextract)
    print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
