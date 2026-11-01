"""Checks for dataset dispatch, attempt preservation, and scheduler configuration."""

from contextlib import redirect_stdout, redirect_stderr
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import run_dataset
from slurm import submit_dataset_jobs

CODE_ROOT = Path(__file__).resolve().parents[1]
SOURCE = "# Preserve verification context\ndef test_state():\n    assert subject() == 1\n"
INTENT = {"objects": ["subject"], "goals": ["Verify subject returns 1"],
          "activities": ["Call subject", "Assert that the result is 1"]}


class Backend:
    model_config = {"model_id": "stub-model"}

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def infer(self, prompt, max_tokens):
        self.calls.append(prompt)
        if not self.responses:
            raise AssertionError("Unexpected inference call")
        response = self.responses.pop(0)
        return response if isinstance(response, str) else json.dumps(response)

    infer_no_thinking = infer


def extraction(intent=INTENT, mode="independent"):
    return [deepcopy(intent)] if mode == "combined" else [
        {key: deepcopy(intent[key])} for key in ("objects", "goals", "activities")]


def supported():
    return [{"supported": True, "unsupported": []}, {"consistent": True, "issues": []}]


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "test_state.py"
        self.source.write_text(SOURCE)
        self.entry = {"path": "Data/Test_Suite/pytest_unit/test_state.py",
                      "git_blob": run_dataset.source_blob(self.source.read_bytes()), "cases": 1}
        self.output = self.root / "results"

    def run_source(self, backend, **kwargs):
        return run_dataset.run_source(self.entry, self.source, service=backend,
                                      output_root=self.output, **kwargs)

    def test_manifest_has_98_sources_and_210_cases(self):
        manifest = run_dataset.load_manifest()
        self.assertEqual(manifest["source_files"], 98)
        self.assertEqual(manifest["test_cases"], 210)
        self.assertEqual(len({row["path"] for row in manifest["sources"]}), 98)

    def test_raw_stage_preserves_the_output_in_all_workflows(self):
        for mode in ("independent", "combined", "chain"):
            with self.subTest(mode=mode):
                backend = Backend(extraction(mode=mode))
                result = self.run_source(backend, mode=mode, stage="raw")
                case = next((Path(result["directory"]) / "cases").iterdir())
                raw = json.loads((case / "raw.json").read_text())
                self.assertEqual({key: raw[key] for key in INTENT}, INTENT)
                self.assertFalse((case / "validated.json").exists())
                self.assertEqual(backend.responses, [])

    def test_raw_empty_output_is_retained_without_selective_retry(self):
        empty = {key: [] for key in INTENT}
        backend = Backend(extraction(empty, mode="combined"))
        result = self.run_source(backend, mode="combined", stage="raw")
        case = next((Path(result["directory"]) / "cases").iterdir())
        self.assertEqual(json.loads((case / "raw.json").read_text())["objects"], [])
        self.assertEqual(result["cases"][0]["extraction_attempts"], 1)

    def test_validated_stage_keeps_raw_and_validated_results(self):
        backend = Backend(extraction() + supported() + [INTENT])
        result = self.run_source(backend)
        case = next((Path(result["directory"]) / "cases").iterdir())
        self.assertTrue((case / "raw.json").is_file())
        validated = json.loads((case / "validated.json").read_text())
        self.assertTrue(validated["validation"]["passed"])
        self.assertEqual(result["failed"], 0)

    def test_validation_retries_keep_the_original_empty_result(self):
        initial = {**INTENT, "goals": []}
        backend = Backend(extraction(initial) + extraction() + supported() + [INTENT])
        result = self.run_source(backend)
        case = next((Path(result["directory"]) / "cases").iterdir())
        self.assertEqual(json.loads((case / "raw.json").read_text())["goals"], [])
        self.assertEqual(json.loads((case / "validated.json").read_text())["goals"], INTENT["goals"])
        self.assertEqual(len(list((case / "attempts").glob("*.json"))), 2)
        self.assertTrue(json.loads((case / "attempts/attempt_001.json").read_text())["validation_feedback"])

    def test_semantic_failure_is_reported_without_losing_raw_output(self):
        backend = Backend(extraction() + [
            {"supported": False, "unsupported": ["unverified condition"]},
            {"consistent": True, "issues": []}])
        result = self.run_source(backend, max_reextract=0)
        case = next((Path(result["directory"]) / "cases").iterdir())
        self.assertEqual(result["failed"], 1)
        self.assertTrue((case / "raw.json").is_file())
        self.assertTrue((case / "error.json").is_file())
        self.assertFalse((case / "validated.json").exists())

    def test_reruns_never_replace_the_first_run(self):
        first = self.run_source(Backend(extraction(mode="combined")), mode="combined", stage="raw")
        original = {p.relative_to(first["directory"]): p.read_bytes()
                    for p in Path(first["directory"]).rglob("*") if p.is_file()}
        second = self.run_source(Backend(extraction(mode="combined")), mode="combined", stage="raw",
                                 run_kind="retry", retry_reason="runtime_failure")
        self.assertNotEqual(first["directory"], second["directory"])
        self.assertTrue(all((Path(first["directory"]) / p).read_bytes() == data for p, data in original.items()))

    def test_empty_output_reruns_are_separate_diagnostics(self):
        with self.assertRaises(ValueError):
            self.run_source(Backend([]), run_kind="retry", retry_reason="empty_output")
        result = self.run_source(Backend(extraction(mode="combined")), mode="combined", stage="raw",
                                 run_kind="diagnostic", retry_reason="empty_output")
        self.assertEqual(result["run_kind"], "diagnostic")
        self.assertEqual(result["retry_reason"], "empty_output")

    def test_modified_source_is_rejected_before_inference(self):
        self.source.write_text(SOURCE + "# changed\n")
        backend = Backend([])
        with self.assertRaisesRegex(ValueError, "differs from the manifest"):
            self.run_source(backend)
        self.assertEqual(backend.calls, [])
        self.assertFalse(self.output.exists())

    def test_case_count_mismatch_is_reported(self):
        self.entry["cases"] = 2
        with self.assertRaisesRegex(ValueError, "number of split cases"):
            self.run_source(Backend([]))


class DispatchTests(unittest.TestCase):
    def test_primary_dry_run_uses_source_count_for_array_bounds(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = submit_dataset_jobs.main(["dataset_gemini_pro.slurm", "--dry-run"])
        details = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertIn("--array=0-97%5", details["command"])
        self.assertEqual(details["test_cases"], 210)

    def test_retry_requires_an_explicit_source_list(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            submit_dataset_jobs.main(["dataset_deepseek_retry.slurm", "--dry-run"])

    def test_empty_output_dispatch_is_labeled_diagnostic(self):
        manifest = run_dataset.load_manifest()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sources.txt"
            path.write_text(manifest["sources"][0]["path"] + "\n")
            output = io.StringIO()
            with redirect_stdout(output):
                submit_dataset_jobs.main(["dataset_deepseek_empty_retry.slurm",
                                          "--file-list", str(path), "--dry-run"])
            details = json.loads(output.getvalue())
        self.assertEqual(details["source_files"], 1)
        self.assertEqual(details["run_kind"], "diagnostic")

    def test_retry_list_rejects_duplicates_or_unknown_files(self):
        manifest = run_dataset.load_manifest()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sources.txt"
            for content in ("unknown.py\n", (manifest["sources"][0]["path"] + "\n") * 2):
                path.write_text(content)
                with self.assertRaises(ValueError):
                    submit_dataset_jobs.select_sources(manifest, path)

    def test_all_scheduler_and_shell_files_parse(self):
        paths = list((CODE_ROOT / "slurm").glob("*.slurm")) + list((CODE_ROOT / "slurm").glob("*.sh"))
        expected_jobs = set(submit_dataset_jobs.JOBS) | {"download_qwen.slurm"}
        self.assertEqual({path.name for path in paths if path.suffix == ".slurm"}, expected_jobs)
        for path in paths:
            subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True)

    def test_primary_wrappers_preserve_the_six_paper_configurations(self):
        expected = {
            "submit_dataset_extraction.slurm": ("qwen", "independent", "local", ""),
            "submit_dataset_combined.slurm": ("qwen", "combined", "local", ""),
            "submit_dataset_chain.slurm": ("qwen", "chain", "local", ""),
            "dataset_deepseek.slurm": ("7b", "independent", "local", ""),
            "dataset_gemini_flash.slurm": ("qwen", "independent", "api", "gemini-2.5-flash"),
            "dataset_gemini_pro.slurm": ("qwen", "independent", "api", "gemini-3.1-pro-preview"),
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "slurm").mkdir()
            for filename in ("job_env.sh", "dataset_job.sh"):
                shutil.copyfile(CODE_ROOT / "slurm" / filename, root / "slurm" / filename)
            stub = root / "fake_python"
            stub.write_text(
                "#!/usr/bin/env python3\nimport json, os, sys\n"
                "print(json.dumps({'args':sys.argv[1:], 'config':[os.getenv(k,'') "
                "for k in ('MODEL_TYPE','EXTRACT_MODE','INFERENCE_BACKEND','GEMINI_MODEL')]}))\n")
            stub.chmod(0o755)
            for filename, config in expected.items():
                environment = {"PATH": os.environ["PATH"], "PROJECT_ROOT": str(root),
                               "PYTHON_BIN": str(stub), "SLURM_ARRAY_TASK_ID": "0"}
                result = subprocess.run(["bash", str(CODE_ROOT / "slurm" / filename)],
                                        env=environment, check=True, capture_output=True, text=True)
                value = json.loads(result.stdout)
                self.assertEqual(value["config"], list(config))
                self.assertIn("--task-index", value["args"])
                self.assertIn("--stage", value["args"])


if __name__ == "__main__":
    unittest.main()
