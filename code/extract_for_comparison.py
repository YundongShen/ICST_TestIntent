import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

from layers.extract import ExtractLayer
from layers.extract.prompts import FIELDS
from layers.input import InputLayer, InputPipeline


class RecordingService:
    def __init__(self, service):
        self.service = service
        self.responses = []

    def infer(self, prompt, max_tokens):
        record = {}
        self.responses.append(record)
        try:
            response = self.service.infer(prompt, max_tokens=max_tokens)
        except Exception as error:
            record.update(response=None, error=f"{type(error).__name__}: {error}")
            return ""
        record["response"] = response
        return response


def run_suite(path, mode="independent", service=None, max_tokens=8000, framework=None):
    if mode not in ("independent", "combined", "chain"):
        raise ValueError("mode must be independent, combined, or chain")
    if max_tokens < 1:
        raise ValueError("max_tokens must be positive")
    path = Path(path)
    cases = InputPipeline().run(str(path))
    if not cases:
        raise ValueError("No test cases found")
    if len({case.case_id for case in cases}) != len(cases):
        raise ValueError("Test case identifiers must be unique")
    if service is None:
        from model.service_factory import get_inference_backend
        service = get_inference_backend()
    configuration = dict(getattr(service, "model_config", {}) or {})
    recorder = RecordingService(service)
    extraction = ExtractLayer(mode, service=recorder, max_tokens=max_tokens)
    records = []
    for raw in InputPipeline.as_records(cases):
        recorder.responses = []
        extracted = extraction.process(InputLayer().process(raw))
        record = {"test_case": raw["test_case_id"]}
        record.update({name: extracted[name] for name in FIELDS})
        record["raw_responses"] = recorder.responses
        records.append(record)
    return {
        "test_case_id": "tc_" + path.stem,
        "source_file": str(path),
        "framework": framework or path.parent.name,
        "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
        "extract_mode": mode,
        "model": getattr(service, "model_name", None) or configuration.get("model_id", "unspecified"),
        "max_tokens": max_tokens,
        "test_cases": records,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--mode", choices=("independent", "combined", "chain"),
                        default=os.getenv("EXTRACT_MODE", "independent"))
    parser.add_argument("--backend", choices=("local", "api"),
                        default=os.getenv("INFERENCE_BACKEND", "local"))
    parser.add_argument("--model")
    parser.add_argument("--framework")
    parser.add_argument("--max-tokens", type=int, default=8000)
    args = parser.parse_args(argv)
    if args.max_tokens < 1:
        parser.error("--max-tokens must be positive")
    if args.model:
        if args.backend == "local" and args.model not in ("qwen", "deepseek", "7b"):
            parser.error("--model must be qwen, deepseek, or 7b for the local backend")
        os.environ["MODEL_TYPE" if args.backend == "local" else "GEMINI_MODEL"] = args.model
    os.environ["INFERENCE_BACKEND"] = args.backend
    target = Path(args.output)
    try:
        if target.exists():
            raise FileExistsError(f"Output already exists: {target}")
        result = run_suite(args.test_file, mode=args.mode, max_tokens=args.max_tokens,
                           framework=args.framework)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        incomplete = sum(
            any(not case[name] for name in FIELDS)
            or any("error" in response for response in case["raw_responses"])
            for case in result["test_cases"])
        print(f"{target}: {len(result['test_cases'])} cases; {incomplete} with empty fields or inference errors")
        return 1 if incomplete else 0
    except (ValueError, RuntimeError, OSError, ImportError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
