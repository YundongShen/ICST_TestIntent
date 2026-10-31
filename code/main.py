#!/usr/bin/env python3
"""Run Test Intent extraction and onboarding generation for a test artifact."""

import argparse
import json
import os
from pathlib import Path
import sys

from layers import BusinessLayer, ExtractLayer, InputLayer, IntentLayer, OutputLayer
from layers.business.onboarding_generator import OnboardingGenerator
from layers.input.pipeline import InputPipeline


def extract_case(raw_data, extract_layer, service=None, levels=None, requirements="", adjust=True,
                 max_reextract=2, merge_activities=False):
    prepared = InputLayer().process(raw_data)
    extracted = extract_layer.process(prepared)
    return IntentLayer(
        extract_layer=extract_layer, service=service, max_reextract=max_reextract, adjust=adjust
    ).process(extracted, levels=levels, requirements=requirements, merge_activities=merge_activities)


def run_pipeline(raw_data, extract_mode=None, service=None, output_dir="Result/onboarding_result",
                 levels=None, requirements="", adjust=True, max_reextract=2, merge_activities=False):

    try:
        extraction = ExtractLayer(extract_mode or os.getenv("EXTRACT_MODE", "independent"), service=service)
        intent = extract_case(raw_data, extraction, service=service, levels=levels,
                              requirements=requirements, adjust=adjust, max_reextract=max_reextract,
                              merge_activities=merge_activities)
        business = BusinessLayer(OnboardingGenerator(service=service)).process(intent)
        output = OutputLayer(output_dir=output_dir).process(business)
        return {"success": output["success"], "output": output, "data": business}
    except (ValueError, RuntimeError) as error:
        return {"success": False, "error": str(error)}


def run_suite(path, extract_mode="independent", service=None, output_dir="Result/onboarding_result",
              levels=None, requirements="", adjust=True, max_reextract=2, merge_activities=False,
              extract_only=False):

    path = Path(path)
    raw_cases = InputPipeline.as_records(InputPipeline().run(str(path)))
    extraction = ExtractLayer(extract_mode=extract_mode, service=service)
    cases = []
    for raw in raw_cases:
        if extract_only:
            cases.append(extraction.process(InputLayer().process(raw)))
        else:
            cases.append(extract_case(
                raw, extraction, service=service, levels=levels, requirements=requirements,
                adjust=adjust, max_reextract=max_reextract, merge_activities=merge_activities))
    result = {"suite_info": {"suite_id": path.name, "dependencies": []},
              "extract_mode": extract_mode, "cases": cases}
    if not extract_only:
        business = BusinessLayer(OnboardingGenerator(service=service)).process(result)
        result["output"] = OutputLayer(output_dir=output_dir).process(business)
        if not result["output"]["success"]:
            raise RuntimeError(result["output"].get("error", "Could not save onboarding report"))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-file", default=os.getenv("TEST_FILE"), help="Test file or suite to process")
    parser.add_argument("--mode", choices=("independent", "combined", "chain"),
                        default=os.getenv("EXTRACT_MODE", "independent"))
    parser.add_argument("--output-dir", default="Result/onboarding_result")
    parser.add_argument("--intent-output", help="Optional JSON path for the case-level results")
    parser.add_argument("--extract-only", action="store_true",
                        help="Run Input and Extract only, without semantic adjustment or onboarding")
    parser.add_argument("--no-adjust", action="store_true", help="Validate without changing granularity")
    parser.add_argument("--object-level", type=float, help="Object granularity, from 0 (specific) to 1 (general)")
    parser.add_argument("--goal-level", type=float, help="Goal granularity, from 0 (specific) to 1 (general)")
    parser.add_argument("--activity-level", type=float, help="Activity granularity, from 0 (specific) to 1 (general)")
    parser.add_argument("--merge-activities", action="store_true",
                        help="Permit adjacent related activities to be grouped during granularity adjustment")
    parser.add_argument("--requirements", default="", help="Downstream task requirements")
    parser.add_argument("--max-reextract", type=int, default=2)
    args = parser.parse_args(argv)
    if not args.test_file:
        parser.error("--test-file or TEST_FILE is required")
    requested = {"objects": args.object_level, "goals": args.goal_level, "activities": args.activity_level}
    levels = {name: value for name, value in requested.items() if value is not None} or None
    try:
        result = run_suite(
            args.test_file, extract_mode=args.mode, output_dir=args.output_dir, levels=levels,
            requirements=args.requirements, adjust=not args.no_adjust,
            max_reextract=args.max_reextract, merge_activities=args.merge_activities,
            extract_only=args.extract_only)
        if args.intent_output:
            target = Path(args.intent_output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
