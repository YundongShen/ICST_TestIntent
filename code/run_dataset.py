#!/usr/bin/env python3
"""Run case-level extraction for one source file, preserving every extraction attempt."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from layers import ExtractLayer, InputLayer, IntentLayer
from layers.extract.prompts import FIELDS, RULES
from layers.input.pipeline import InputPipeline

CODE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = CODE_ROOT.parent
DEFAULT_MANIFEST = CODE_ROOT / "slurm" / "test_suite_manifest.json"


def load_manifest(path=DEFAULT_MANIFEST):
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("The manifest has no source files")
    paths = [entry["path"] for entry in sources]
    if len(paths) != len(set(paths)):
        raise ValueError("The manifest contains duplicate source files")
    if manifest.get("source_files") != len(sources) or manifest.get("test_cases") != sum(entry["cases"] for entry in sources):
        raise ValueError("Manifest totals do not match its source records")
    return manifest


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as target:
        json.dump(value, target, ensure_ascii=False, indent=2)
        target.write("\n")


def source_blob(content):
    return hashlib.sha1(("blob " + str(len(content)) + "\0").encode() + content).hexdigest()


class RecordingExtractor:
    def __init__(self, extractor, directory):
        self.extractor = extractor
        self.directory = directory
        self.attempts = 0

    def process(self, payload):
        attempt = self.attempts
        self.attempts += 1
        result = self.extractor.process(payload)
        write_json(self.directory / f"attempt_{attempt:03d}.json", {
            "attempt": attempt, "validation_feedback": payload.get("extraction_feedback", ""),
            "intent": {name: result.get(name, []) for name in FIELDS}})
        return result


def run_source(entry, source_path, service=None, mode="independent", output_root=None,
               stage="validated", run_kind="primary", retry_reason="", max_reextract=2,
               manifest=DEFAULT_MANIFEST):
    if stage not in ("raw", "validated"):
        raise ValueError("stage must be raw or validated")
    if run_kind not in ("primary", "retry", "diagnostic"):
        raise ValueError("Unknown run kind")
    if run_kind != "primary" and retry_reason not in ("runtime_failure", "missing_output", "empty_output"):
        raise ValueError("A retry reason is required for reruns")
    if retry_reason == "empty_output" and run_kind != "diagnostic":
        raise ValueError("Empty-output reruns must be recorded as diagnostic runs")
    if mode not in ("independent", "combined", "chain"):
        raise ValueError("Unknown extraction mode")
    source_path = Path(source_path)
    if source_blob(source_path.read_bytes()) != entry["git_blob"]:
        raise ValueError("Source file differs from the manifest: " + entry["path"])
    cases = InputPipeline().run(str(source_path))
    if len(cases) != entry["cases"]:
        raise ValueError("The number of split cases differs from the manifest: " + entry["path"])
    if service is None:
        from model.service_factory import get_inference_backend
        service = get_inference_backend()
    configuration = dict(getattr(service, "model_config", {}) or {})
    model = getattr(service, "model_name", None) or configuration.get("model_id", "unspecified")
    label = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(model)) + "_" + mode
    output_root = Path(output_root) if output_root else CODE_ROOT / "Result" / "dataset"
    parent = output_root / run_kind / label
    parent.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix="run_", dir=parent))
    metadata = {
        "source_file": entry["path"], "source_git_blob": entry["git_blob"],
        "manifest": str(Path(manifest).resolve()), "mode": mode, "model": model,
        "stage": stage, "run_kind": run_kind, "retry_reason": retry_reason,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "slurm_job_id": os.getenv("SLURM_JOB_ID", ""),
        "slurm_array_task_id": os.getenv("SLURM_ARRAY_TASK_ID", ""),
        "case_count": len(cases), "max_reextract": max_reextract,
        "extraction_rules_sha256": hashlib.sha256(json.dumps(RULES, sort_keys=True).encode()).hexdigest(),
    }
    write_json(run_dir / "run.json", metadata)
    statuses = []
    extraction = ExtractLayer(extract_mode=mode, service=service)
    for raw in InputPipeline.as_records(cases):
        case_dir = run_dir / "cases" / raw["test_case_id"]
        case_dir.mkdir(parents=True, exist_ok=False)
        prepared = InputLayer().process(raw)
        write_json(case_dir / "source.json", prepared)
        recorder = RecordingExtractor(extraction, case_dir / "attempts")
        try:
            initial = recorder.process(prepared)
            write_json(case_dir / "raw.json", initial)
            if stage == "validated":
                final = IntentLayer(extract_layer=recorder, service=service,
                                    max_reextract=max_reextract).process(initial)
                write_json(case_dir / "validated.json", final)
            status = {"test_case_id": raw["test_case_id"], "status": "completed",
                      "stage": stage, "extraction_attempts": recorder.attempts}
        except Exception as error:
            status = {"test_case_id": raw["test_case_id"], "status": "failed",
                      "error_type": type(error).__name__, "error": str(error),
                      "extraction_attempts": recorder.attempts}
            write_json(case_dir / "error.json", status)
        statuses.append(status)
    summary = {**metadata, "finished_at": datetime.now(timezone.utc).isoformat(),
               "failed": sum(row["status"] == "failed" for row in statuses), "cases": statuses}
    write_json(run_dir / "summary.json", summary)
    return {"directory": str(run_dir), **summary}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--task-index", type=int, default=int(os.getenv("SLURM_ARRAY_TASK_ID", "0")))
    parser.add_argument("--mode", choices=("independent", "combined", "chain"), default="independent")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--stage", choices=("raw", "validated"), default="validated")
    parser.add_argument("--run-kind", choices=("primary", "retry", "diagnostic"), default="primary")
    parser.add_argument("--retry-reason", choices=("runtime_failure", "missing_output", "empty_output"), default="")
    parser.add_argument("--max-reextract", type=int, default=2)
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        if not 0 <= args.task_index < len(manifest["sources"]):
            raise ValueError("task-index is outside the manifest")
        entry = manifest["sources"][args.task_index]
        result = run_source(entry, REPO_ROOT / entry["path"], mode=args.mode,
                            output_root=args.output_root, stage=args.stage,
                            run_kind=args.run_kind, retry_reason=args.retry_reason,
                            max_reextract=args.max_reextract, manifest=args.manifest)
        print(json.dumps({"directory": result["directory"], "cases": result["case_count"],
                          "failed": result["failed"], "stage": result["stage"]}))
        return 1 if result["failed"] else 0
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
