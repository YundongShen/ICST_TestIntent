"""Regression tests for extraction rules and the semantic processing pipeline."""

from contextlib import nullcontext
from copy import deepcopy
import importlib
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

from layers import ExtractLayer, InputLayer, IntentLayer
from layers.business import BusinessLayer
from layers.business.onboarding_generator import OnboardingGenerator
from layers.extract.prompts import RULES
from layers.input.pipeline import InputPipeline
from layers.input.preprocessor import Preprocessor
from layers.intent.granularity_adjuster import GranularityAdjuster, GranularityAdjustmentError
from layers.intent.semantic_layer import SemanticLayer, SemanticValidationError
from layers.intent.semantic_validator import SemanticValidator
from layers.json_utils import parse_json
from main import run_pipeline, run_suite

SOURCE = '# Preserve this explanation\ndef test_link():\n    left.prepare()\n    assert right.read() == 2\n'
INTENT = {
    "objects": ["left.prepare", "right.read"],
    "goals": ["Verify the prepared state is read as 2"],
    "activities": ["Prepare state with left.prepare", "Call right.read and assert the result is 2"],
}


def encoded(value):
    return json.dumps(value, ensure_ascii=False)


class Backend:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def infer(self, prompt, max_tokens):
        self.calls.append((prompt, max_tokens))
        if not self.responses:
            raise AssertionError("Unexpected inference call")
        value = self.responses.pop(0)
        return value if isinstance(value, str) else encoded(value)

    infer_no_thinking = infer


def extraction_responses(mode, intent=None):
    intent = INTENT if intent is None else intent
    return [intent] if mode == "combined" else [{name: intent[name]} for name in ("objects", "goals", "activities")]


def valid_report_responses():
    return [{"supported": True, "unsupported": []}, {"consistent": True, "issues": []}]


class InputTests(unittest.TestCase):
    def test_preprocessing_preserves_comments_strings_and_whitespace(self):
        source = '# purpose\r\ndef test_x():\r\n\tvalue = """\r\n# literal value\r\n// literal value\r\n\r\n"""\r\n\tassert value\r\n'
        self.assertEqual(InputLayer().process({"content": source})["content"], source)

    def test_process_file_returns_content_and_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test_x.py"
            source = "# keep\r\ndef test_x():\r\n    assert True\r\n"
            path.write_bytes(source.encode())
            result = Preprocessor().process_file(path)
            self.assertEqual(result["content"], source)
            self.assertEqual(result["file_name"], path.name)

    def test_suite_splitting_keeps_comments_imports_and_setup(self):
        source = """import helpers from './helpers';
// shared explanation
describe('state', () => {
  beforeEach(() => { prepare(); });
  test('one', () => { expect(read()).toBe(1); });
  test('two', () => { expect(read()).toBe(2); });
});
"""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.test.js"
            path.write_text(source)
            cases = InputPipeline().run(str(path))
        self.assertEqual(len(cases), 2)
        for case in cases:
            self.assertIn("// shared explanation", case.source)
            self.assertIn("import helpers", case.source)
            self.assertIn("beforeEach", case.source)
        self.assertNotIn("test('two'", cases[0].source)
        self.assertNotIn("test('one'", cases[1].source)


class ExtractionTests(unittest.TestCase):
    def test_all_workflows_use_the_same_rules_and_keep_multiple_objects(self):
        for mode in ("independent", "combined", "chain"):
            with self.subTest(mode=mode):
                backend = Backend(extraction_responses(mode))
                result = ExtractLayer(mode, service=backend).process({"content": SOURCE})
                self.assertEqual({name: result[name] for name in INTENT}, INTENT)
                self.assertEqual(len(backend.calls), 1 if mode == "combined" else 3)
                self.assertEqual({limit for _, limit in backend.calls}, {8000})
                for prompt, _ in backend.calls:
                    self.assertIn(SOURCE, prompt)
                if mode == "combined":
                    self.assertTrue(all(rule in backend.calls[0][0] for rule in RULES.values()))
                else:
                    for (prompt, _), name in zip(backend.calls, ("objects", "goals", "activities")):
                        self.assertIn(RULES[name], prompt)
                if mode == "chain":
                    self.assertIn("[Previously Extracted Objects]", backend.calls[1][0])
                    self.assertIn("[Previously Extracted Goals]", backend.calls[2][0])
                else:
                    self.assertTrue(all("[Previously Extracted" not in prompt for prompt, _ in backend.calls))

    def test_indirectly_assessed_system_methods_are_not_excluded(self):
        backend = Backend(extraction_responses("combined"))
        ExtractLayer("combined", service=backend).process({"content": SOURCE})
        prompt = backend.calls[0][0]
        self.assertIn("both\n   methods can be Test Objects", prompt)
        self.assertNotIn("Output: a single string", prompt)
        self.assertNotIn("Retain only entities that are the direct, primary target", prompt)

    def test_parser_reads_final_json_with_unicode_and_quoted_braces(self):
        expected = {"objects": ["méthode('{')", 'target("}")']}
        text = '<think>{"objects":["wrong"]}</think>\n{"objects":["object1"]}\n' + encoded(expected)
        self.assertEqual(parse_json(text, ("objects",)), expected)

    def test_combined_uses_final_answer_instead_of_an_earlier_template(self):
        response = '{"objects":["object1"],"goals":["string1"],"activities":["action1"]}\n' + encoded(INTENT)
        result = ExtractLayer("combined", service=Backend([response])).process({"content": SOURCE})
        self.assertEqual(result["objects"], INTENT["objects"])

    def test_invalid_mode_is_reported(self):
        with self.assertRaises(ValueError):
            ExtractLayer("typo")


class ValidationTests(unittest.TestCase):
    def test_validator_checks_the_complete_source_artifact(self):
        backend = Backend(valid_report_responses())
        report = SemanticValidator(service=backend).validate(INTENT, SOURCE)
        self.assertTrue(report.passed)
        self.assertIn(SOURCE, backend.calls[0][0])

    def test_missing_source_is_rejected(self):
        with self.assertRaises(ValueError):
            SemanticValidator(service=Backend([])).validate(INTENT, "")

    def test_string_false_is_not_accepted_as_true(self):
        backend = Backend([{"supported": "false", "unsupported": []}, {"consistent": True, "issues": []}])
        self.assertFalse(SemanticValidator(service=backend).validate(INTENT, SOURCE).passed)

    def test_nonstring_descriptions_fail_completeness_without_inference(self):
        invalid = {**INTENT, "goals": [None]}
        backend = Backend([])
        report = SemanticValidator(service=backend).validate(invalid, SOURCE)
        self.assertFalse(report.complete)
        self.assertEqual(backend.calls, [])

    def test_reextraction_receives_feedback_and_keeps_case_metadata(self):
        initial = {**INTENT, "goals": [], "content": SOURCE, "test_case_id": "case-a"}
        backend = Backend(extraction_responses("chain") + valid_report_responses())
        extraction = ExtractLayer("chain", service=backend)
        result = IntentLayer(extraction, service=backend, adjust=False).process(initial)
        self.assertTrue(result["validation"]["passed"])
        self.assertEqual(result["reextract_count"], 1)
        self.assertEqual(result["test_case_id"], "case-a")
        self.assertEqual(result["content"], SOURCE)
        for prompt, _ in backend.calls[:3]:
            self.assertIn("[Validation Feedback]", prompt)
            self.assertIn("goals must contain", prompt)

    def test_failed_support_check_causes_reextraction(self):
        responses = [{"supported": False, "unsupported": ["invented condition"]},
                     {"consistent": True, "issues": []}]
        responses += extraction_responses("combined") + valid_report_responses()
        backend = Backend(responses)
        layer = IntentLayer(ExtractLayer("combined", service=backend), service=backend, adjust=False)
        result = layer.process({**INTENT, "content": SOURCE})
        self.assertEqual(result["reextract_count"], 1)
        self.assertIn("invented condition", backend.calls[2][0])

    def test_failed_validation_stops_after_the_retry_limit(self):
        calls = []
        invalid = {**INTENT, "goals": []}
        def retry(source, feedback):
            calls.append((source, feedback))
            return deepcopy(invalid)
        layer = SemanticLayer(extractor=retry, validator=SemanticValidator(service=Backend([])),
                              max_reextract=2, adjust=False)
        with self.assertRaises(SemanticValidationError):
            layer.process(invalid, SOURCE)
        self.assertEqual(len(calls), 2)


class GranularityTests(unittest.TestCase):
    def test_only_selected_elements_change(self):
        answer = {**INTENT, "objects": ["unrelated"], "goals": ["Verify consistency of prepared and read state"]}
        backend = Backend([answer, {"preserved": True, "issues": []}])
        result = GranularityAdjuster(service=backend).adjust(INTENT, levels={"goals": 0.8})
        self.assertEqual(result["objects"], INTENT["objects"])
        self.assertEqual(result["activities"], INTENT["activities"])
        self.assertEqual(result["goals"], answer["goals"])
        self.assertEqual(INTENT["goals"], ["Verify the prepared state is read as 2"])

    def test_unsupported_semantic_change_is_rejected(self):
        answer = {**INTENT, "goals": ["Verify all invalid inputs are rejected"]}
        backend = Backend([answer, {"preserved": False, "issues": ["new verification condition"]}])
        with self.assertRaises(GranularityAdjustmentError):
            GranularityAdjuster(service=backend).adjust(INTENT, levels={"goals": 0.8})

    def test_unreadable_preservation_check_is_rejected(self):
        answer = {**INTENT, "goals": ["Verify state consistency"]}
        backend = Backend([answer, '{"preserved":"false","issues":[]}'])
        with self.assertRaises(GranularityAdjustmentError):
            GranularityAdjuster(service=backend).adjust(INTENT, levels={"goals": 0.8})

    def test_activity_merging_requires_explicit_request(self):
        answer = {**INTENT, "activities": ["Prepare state and check that reading it returns 2"]}
        with self.assertRaises(GranularityAdjustmentError):
            GranularityAdjuster(service=Backend([answer])).adjust(INTENT, levels={"activities": 0.8})
        backend = Backend([answer, {"preserved": True, "issues": []}])
        result = GranularityAdjuster(service=backend).adjust(
            INTENT, levels={"activities": 0.8}, merge_activities=True)
        self.assertEqual(len(result["activities"]), 1)

    def test_invalid_granularity_levels_are_rejected(self):
        for value in (-1, 2, float("nan"), float("inf"), True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                GranularityAdjuster(service=Backend([])).adjust(INTENT, levels={"goals": value})

    def test_adjusted_output_is_revalidated_against_source(self):
        answer = {**INTENT, "goals": ["Verify state consistency"]}
        responses = extraction_responses("combined") + valid_report_responses()
        responses += [answer, {"preserved": True, "issues": []},
                      {"supported": False, "unsupported": ["overstated check"]},
                      {"consistent": True, "issues": []}]
        backend = Backend(responses)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "reports"
            result = run_pipeline({"content": SOURCE, "test_case_id": "case-a"},
                                  "combined", service=backend, output_dir=str(output),
                                  levels={"goals": 0.8}, max_reextract=0)
            self.assertFalse(result["success"])
            self.assertFalse(output.exists())
        self.assertEqual(backend.responses, [])


class PipelineTests(unittest.TestCase):
    def test_all_workflows_generate_a_report_after_validation_and_adjustment(self):
        for mode in ("independent", "combined", "chain"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                responses = extraction_responses(mode) + valid_report_responses()
                responses += [INTENT, {"groups": [{"shared_question": "Is prepared state read correctly?",
                                                  "test_case_ids": ["case-a"]}]},
                              "## Test Suite Overview\nValidated suite summary"]
                backend = Backend(responses)
                result = run_pipeline({"content": SOURCE, "test_case_id": "case-a"}, mode,
                                      service=backend, output_dir=temp)
                self.assertTrue(result["success"], result)
                self.assertTrue(result["data"]["validation"]["passed"])
                self.assertTrue(Path(result["output"]["filepath"]).is_file())
                self.assertEqual(backend.responses, [])

    def test_invalid_intent_does_not_reach_document_generation(self):
        responses = extraction_responses("combined", {**INTENT, "goals": []})
        backend = Backend(responses)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "not-created"
            result = run_pipeline({"content": SOURCE}, "combined", service=backend,
                                  output_dir=str(output), max_reextract=0)
            self.assertFalse(result["success"])
            self.assertFalse(output.exists())
        self.assertEqual(backend.responses, [])

    def test_full_suite_is_processed_case_by_case(self):
        source = '# suite purpose\ndef test_one():\n    assert read() == 1\n\ndef test_two():\n    assert read() == 2\n'
        responses = []
        for _ in range(2):
            responses += extraction_responses("combined") + valid_report_responses()
        responses += [{"groups": [{"shared_question": "Is prepared state read correctly?",
                                    "test_case_ids": ["test_state_1", "test_state_2"]}]},
                      "## Test Suite Overview\nTwo validated cases"]
        backend = Backend(responses)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test_state.py"
            path.write_text(source)
            result = run_suite(path, "combined", service=backend, output_dir=temp, adjust=False)
        self.assertEqual(len(result["cases"]), 2)
        self.assertTrue(all(case["validation"]["passed"] for case in result["cases"]))
        self.assertEqual(backend.responses, [])

    def test_extract_only_does_not_run_semantic_or_document_steps(self):
        backend = Backend(extraction_responses("combined"))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "test_state.py"
            path.write_text(SOURCE)
            result = run_suite(path, "combined", service=backend, extract_only=True)
        self.assertNotIn("output", result)
        self.assertEqual(len(backend.calls), 1)

    def test_business_rejects_unvalidated_intent(self):
        with self.assertRaises(ValueError):
            BusinessLayer(OnboardingGenerator(service=Backend([]))).process(INTENT)

    def test_grouping_rejects_duplicate_or_unknown_cases(self):
        for ids in (["a", "a"], ["other"]):
            backend = Backend([{"groups": [{"shared_question": "Check state?", "test_case_ids": ids}]}])
            result = OnboardingGenerator(service=backend).group_cases(
                "suite", [{"id": "a", "object": "state", "goal": "check state"}])
            self.assertEqual(result["status"], "error")

    def test_empty_document_is_reported_as_a_failure(self):
        backend = Backend([""])
        result = OnboardingGenerator(service=backend)._generate_with_model("format")
        self.assertEqual(result["status"], "error")

    def test_main_import_does_not_load_a_model(self):
        with patch("model.service_factory.get_inference_backend", side_effect=AssertionError):
            importlib.reload(importlib.import_module("main"))


class LocalInferenceTests(unittest.TestCase):
    def _inference(self, length, context):
        from model.inference_service import InferenceService
        tensor = types.SimpleNamespace(shape=(1, length))
        class Inputs(dict):
            def to(self, device):
                return self
        class Tokenizer:
            pad_token_id = 0
            eos_token_id = 1
            options = None
            def apply_chat_template(self, messages, **kwargs):
                return messages[0]["content"]
            def __call__(self, text, **kwargs):
                self.options = kwargs
                return Inputs(input_ids=tensor, attention_mask=None)
            def decode(self, ids, **kwargs):
                return '{"objects":["méthode"]}'
        class Model:
            options = None
            def eval(self):
                pass
            def generate(self, **kwargs):
                self.options = kwargs
                return [[0] * length + [1]]
        tokenizer, model = Tokenizer(), Model()
        service = InferenceService(model_config={"model_id": "Qwen/Qwen3.5-27B", "context_length": context})
        service._load_local_model = lambda: (model, tokenizer, "cpu")
        return service, tokenizer, model

    def test_complete_prompt_is_not_silently_truncated_and_unicode_is_preserved(self):
        service, tokenizer, model = self._inference(2300, 4096)
        with patch.dict("sys.modules", {"torch": types.SimpleNamespace(no_grad=nullcontext)}):
            response = service.infer("source", max_tokens=8000)
        self.assertFalse(tokenizer.options["truncation"])
        self.assertFalse(tokenizer.options["add_special_tokens"])
        self.assertEqual(model.options["max_new_tokens"], 1796)
        self.assertIn("méthode", response)

    def test_overlong_prompt_is_reported_before_generation(self):
        service, tokenizer, model = self._inference(4096, 4096)
        with patch.dict("sys.modules", {"torch": types.SimpleNamespace(no_grad=nullcontext)}):
            with self.assertRaisesRegex(ValueError, "exceeds the configured context"):
                service.infer("source")
        self.assertIsNone(model.options)


if __name__ == "__main__":
    unittest.main()

