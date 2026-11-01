from contextlib import ExitStack, redirect_stdout, redirect_stderr
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from extract_for_comparison import main, run_suite
from tests.test_extraction_pipeline import Backend, INTENT, extraction_responses


SOURCE = """import helper from './helper';
// shared explanation
describe('state', () => {
  beforeEach(() => { prepare(); });
  test('one', () => { expect(read()).toBe(1); });
  test('two', () => { expect(read()).toBe(2); });
});
"""


class ComparisonExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "state.test.js"
        self.path.write_text(SOURCE, encoding="utf-8")
        self.output = Path(self.temp.name) / "state.testIntent.json"

    def test_all_workflows_extract_cases_separately_without_downstream_layers(self):
        blocked = (
            "layers.intent.IntentLayer.__init__",
            "layers.intent.semantic_layer.SemanticLayer.__init__",
            "layers.intent.semantic_validator.SemanticValidator.__init__",
            "layers.intent.granularity_adjuster.GranularityAdjuster.__init__",
            "layers.business.BusinessLayer.__init__",
            "layers.output.OutputLayer.__init__",
        )
        for mode in ("independent", "combined", "chain"):
            with self.subTest(mode=mode), ExitStack() as stack:
                for name in blocked:
                    stack.enter_context(patch(name, side_effect=AssertionError(name)))
                backend = Backend(extraction_responses(mode) * 2)
                result = run_suite(self.path, mode=mode, service=backend, max_tokens=1234)
                cases = result["test_cases"]
                self.assertEqual([case["test_case"] for case in cases], ["state.test_1", "state.test_2"])
                for case in cases:
                    self.assertEqual({name: case[name] for name in INTENT}, INTENT)
                per_case = 1 if mode == "combined" else 3
                self.assertEqual(len(backend.calls), per_case * 2)
                for index, (prompt, limit) in enumerate(backend.calls):
                    self.assertEqual(limit, 1234)
                    self.assertIn("// shared explanation", prompt)
                    self.assertIn("beforeEach", prompt)
                    self.assertIn("import helper", prompt)
                    self.assertIn("test('one'" if index < per_case else "test('two'", prompt)
                    self.assertNotIn("test('two'" if index < per_case else "test('one'", prompt)
                self.assertTrue(all(len(case["raw_responses"]) == per_case for case in cases))

    def test_invalid_outputs_are_saved_without_reextracting_or_dropping_cases(self):
        backend = Backend(["<think>reasoning only</think>", INTENT])
        result = run_suite(self.path, mode="combined", service=backend)
        self.assertEqual(len(backend.calls), 2)
        self.assertEqual(len(result["test_cases"]), 2)
        first, second = result["test_cases"]
        self.assertEqual({name: first[name] for name in INTENT}, {name: [] for name in INTENT})
        self.assertEqual(first["raw_responses"], [{"response": "<think>reasoning only</think>"}])
        self.assertEqual(second["objects"], INTENT["objects"])

    def test_inference_error_does_not_remove_other_elements_or_cases(self):
        backend = Backend(extraction_responses("independent") * 2)
        original = backend.infer
        calls = []

        def infer(prompt, max_tokens):
            calls.append(prompt)
            if len(calls) == 2:
                backend.responses.pop(0)
                raise RuntimeError("unavailable")
            return original(prompt, max_tokens)

        backend.infer = infer
        result = run_suite(self.path, service=backend)
        self.assertEqual(len(calls), 6)
        first, second = result["test_cases"]
        self.assertEqual(first["goals"], [])
        self.assertEqual(first["objects"], INTENT["objects"])
        self.assertEqual(first["activities"], INTENT["activities"])
        self.assertEqual(first["raw_responses"][1]["error"], "RuntimeError: unavailable")
        self.assertEqual(second["goals"], INTENT["goals"])

    def test_cli_selects_backends_and_writes_one_suite_json(self):
        for backend_name, model, variable in (
            ("local", "qwen", "MODEL_TYPE"),
            ("local", "deepseek", "MODEL_TYPE"),
            ("api", "gemini-2.5-flash", "GEMINI_MODEL"),
            ("api", "gemini-3.1-pro-preview", "GEMINI_MODEL"),
        ):
            with self.subTest(model=model), patch.dict(os.environ), redirect_stdout(io.StringIO()):
                backend = Backend(extraction_responses("combined") * 2)
                backend.model_name = model
                def factory():
                    self.assertEqual(os.environ["INFERENCE_BACKEND"], backend_name)
                    self.assertEqual(os.environ[variable], model)
                    return backend
                target = self.output.with_name(model + ".json")
                with patch("model.service_factory.get_inference_backend", side_effect=factory):
                    code = main(["--test-file", str(self.path), "--output", str(target),
                                 "--mode", "combined", "--backend", backend_name, "--model", model,
                                 "--framework", "jest"])
                self.assertEqual(code, 0)
                result = json.loads(target.read_text())
                self.assertEqual(result["model"], model)
                self.assertEqual(result["framework"], "jest")
                self.assertEqual(result["test_case_id"], "tc_state.test")
                self.assertEqual(len(result["test_cases"]), 2)

    def test_cli_reports_empty_results_and_prevents_overwriting_before_inference(self):
        backend = Backend(["", INTENT])
        args = ["--test-file", str(self.path), "--output", str(self.output), "--mode", "combined"]
        with patch.dict(os.environ), patch("model.service_factory.get_inference_backend", return_value=backend), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(args), 1)
            saved = self.output.read_bytes()
            self.assertEqual(len(json.loads(saved)["test_cases"]), 2)
            self.assertEqual(main(args), 1)
            self.assertEqual(self.output.read_bytes(), saved)
            self.assertEqual(len(backend.calls), 2)


if __name__ == "__main__":
    unittest.main()
