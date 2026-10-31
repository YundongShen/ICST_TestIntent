#!/usr/bin/env python3
"""Submit dataset jobs with array bounds derived from the selected source manifest."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

CODE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE_ROOT))
from run_dataset import DEFAULT_MANIFEST, load_manifest

JOBS = {
    "submit_dataset_extraction.slurm": (30, False, ""),
    "submit_dataset_combined.slurm": (30, False, ""),
    "submit_dataset_chain.slurm": (30, False, ""),
    "dataset_deepseek.slurm": (15, False, ""),
    "dataset_gemini_flash.slurm": (10, False, ""),
    "dataset_gemini_pro.slurm": (5, False, ""),
    "dataset_combined_missing.slurm": (10, True, "missing_output"),
    "dataset_combined_empty_retry.slurm": (4, True, "empty_output"),
    "dataset_deepseek_retry.slurm": (15, True, "runtime_failure"),
    "dataset_deepseek_empty_retry.slurm": (5, True, "empty_output"),
    "dataset_gemini_flash_retry.slurm": (10, True, ""),
}


def select_sources(manifest, file_list=None):
    if file_list is None:
        return list(manifest["sources"])
    by_path = {row["path"]: row for row in manifest["sources"]}
    selected = []
    for line in Path(file_list).read_text(encoding="utf-8").splitlines():
        path = line.strip()
        if not path or path.startswith("#"):
            continue
        candidate = Path(path)
        if candidate.is_absolute():
            try:
                path = candidate.resolve().relative_to(CODE_ROOT.parent.resolve()).as_posix()
            except ValueError:
                raise ValueError("A retry file is outside this repository")
        if path not in by_path:
            raise ValueError("A selected file is absent from the source manifest: " + path)
        selected.append(by_path[path])
    if not selected or len({row["path"] for row in selected}) != len(selected):
        raise ValueError("The selected file list is empty or contains duplicates")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", choices=sorted(JOBS))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--file-list", type=Path, help="Explicit source paths for a subset or retry run")
    parser.add_argument("--retry-reason", choices=("runtime_failure", "missing_output", "empty_output"))
    parser.add_argument("--stage", choices=("raw", "validated"), default="validated")
    parser.add_argument("--max-parallel", type=int)
    parser.add_argument("--dry-run", action="store_true", help="Print submission details without submitting a job")
    args = parser.parse_args(argv)
    parallel, is_retry, default_reason = JOBS[args.job]
    try:
        if is_retry and args.file_list is None:
            raise ValueError("Retry jobs require an explicit --file-list")
        reason = args.retry_reason or default_reason
        if is_retry and not reason:
            raise ValueError("Specify --retry-reason for this retry job")
        if not is_retry and args.retry_reason:
            raise ValueError("A primary job cannot be labeled as a retry")
        parallel = args.max_parallel if args.max_parallel is not None else parallel
        if parallel < 1:
            raise ValueError("max-parallel must be positive")
        manifest = load_manifest(args.manifest)
        selected = select_sources(manifest, args.file_list)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    kind = "diagnostic" if is_retry and reason == "empty_output" else "retry" if is_retry else "primary"
    command = ["sbatch", "--chdir", str(CODE_ROOT), f"--array=0-{len(selected) - 1}%{parallel}",
               str(CODE_ROOT / "slurm" / args.job)]
    details = {"command": command, "source_files": len(selected),
               "test_cases": sum(row["cases"] for row in selected), "run_kind": kind,
               "retry_reason": reason, "stage": args.stage}
    if args.dry_run:
        print(json.dumps(details, indent=2))
        return 0
    selection_dir = CODE_ROOT / "Result" / "slurm_manifests"
    selection_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", prefix="selection_",
                                     dir=selection_dir, delete=False, encoding="utf-8") as target:
        selection = {"source_files": len(selected), "test_cases": sum(row["cases"] for row in selected),
                     "sources": selected}
        json.dump(selection, target, indent=2)
        selected_manifest = target.name
    (CODE_ROOT / "logs").mkdir(exist_ok=True)
    environment = dict(os.environ, PROJECT_ROOT=str(CODE_ROOT), MANIFEST_PATH=selected_manifest,
                       RUN_KIND=kind, RETRY_REASON=reason, DATASET_STAGE=args.stage)
    subprocess.run(command, env=environment, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
