from copy import deepcopy
import os
from pathlib import Path
import tempfile
import unittest
from urllib.parse import unquote

from layers.business import BusinessLayer
from layers.business.onboarding_generator import OnboardingGenerator
from layers.business.onboarding_template import PROMPT
from layers.input.metadata import case_metadata, declared_dependencies
from layers.input.pipeline import InputPipeline
from main import run_suite
from tests.test_extraction_pipeline import Backend, INTENT, extraction_responses, valid_report_responses


class CapturingGenerator:
    def group_cases(self, suite_id, cases):
        self.cases = cases
        return {"status": "success", "groups": [{"shared_question": "What is verified?",
                "test_case_ids": [case["id"] for case in cases]}]}

    def generate_suite_document(self, template, suite_info, cases, groups):
        self.suite_info = suite_info
        self.prompt = OnboardingGenerator._build_suite_prompt(template, suite_info, cases, groups)
        return {"status": "success", "document": "## Test Suite Overview\nRecorded metadata"}


class OnboardingMetadataTests(unittest.TestCase):
    def test_javascript_imports_are_read_without_comments_or_string_false_positives(self):
        source = '''import './setup'
import {
  test, expect
} from '@playwright/test';
const request = require(
  /* module */ 'supertest'
);
import { value /* from 'wrong-comment' */ } from './helper';
import type { Result } from './types';
import '@playwright/test';
export { something } from './exported';
const loading = import('./dynamic');
// import 'wrong-line-comment';
const text = "require('wrong-string')";
/* require('wrong-block-comment'); */
'''
        self.assertEqual(declared_dependencies(source, "code/javascript"),
                         ["./setup", "@playwright/test", "supertest", "./helper", "./types", "./exported", "./dynamic"])

    def test_python_and_java_dependencies_come_from_imports(self):
        python = '''import os, json
from package.client import Client
from . import helpers
from ..shared import prepare
text = "import fake"
'''
        self.assertEqual(declared_dependencies(python, "code/python"),
                         ["os", "json", "package.client", ".helpers", "..shared"])
        java = '''package example;
import org.junit.Test;
import static org.junit.Assert.*;
// import fake.Package;
String text = "import wrong.Package;";
'''
        self.assertEqual(declared_dependencies(java, "code/java"), ["org.junit.Test", "org.junit.Assert.*"])
        self.assertEqual(declared_dependencies("import fake", "manual"), [])
        self.assertEqual(declared_dependencies("broken Python !!!", "code/python"), [])

    def test_actual_survey_suite_metadata_reaches_the_generation_prompt(self):
        repo = Path(__file__).resolve().parents[2]
        source = repo / "Data/Test_Suite/playwright/module.spec.ts"
        cases = InputPipeline.as_records(InputPipeline().run(str(source)))
        self.assertEqual(len(cases), 6)
        for case in cases:
            case.update(deepcopy(INTENT), validation={"passed": True})
            self.assertEqual(case["context"]["dependencies"], ["@playwright/test"])
        before = deepcopy(cases)
        generator = CapturingGenerator()
        with tempfile.TemporaryDirectory() as directory:
            result = BusinessLayer(generator).process({"suite_info": {"suite_id": source.name, "dependencies": []},
                                                       "cases": cases}, output_dir=directory)
            self.assertEqual(generator.suite_info["dependencies"], ["@playwright/test"])
            for original, received in zip(cases, generator.cases):
                self.assertEqual(received["dependencies"], ["@playwright/test"])
                start, end = original["context"]["line_range"]
                expected = f"[{source.name}:{start}-{end}]({Path(os.path.relpath(source.resolve(), Path(directory).resolve())).as_posix()}#L{start}-L{end})"
                self.assertEqual(received["source_reference"], expected)
                self.assertIn(expected, generator.prompt)
                self.assertEqual(received["activities"], original["activities"])
                self.assertEqual(received["source_file"], str(source))
            self.assertEqual(result["suite_info"]["dependencies"], ["@playwright/test"])
        self.assertEqual(cases, before)

    def test_main_carries_metadata_through_validation_to_the_document_prompt(self):
        source = """import { test, expect } from '@playwright/test';
test('first', () => { expect(1).toBe(1); });
test('second', () => { expect(2).toBe(2); });
"""
        responses = []
        for _ in range(2):
            responses += extraction_responses("combined") + valid_report_responses()
        responses += [{"groups": [{"shared_question": "What is verified?", "test_case_ids": ["page.test_1", "page.test_2"]}]},
                      "## Test Suite Overview\nRecorded metadata"]
        backend = Backend(responses)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "page.test.js"
            path.write_text(source)
            output = root / "reports"
            result = run_suite(path, "combined", service=backend, output_dir=output, adjust=False)
            self.assertEqual(result["suite_info"]["dependencies"], ["@playwright/test"])
            self.assertIn("[page.test.js:2-2](../page.test.js#L2-L2)", backend.calls[-1][0])
            self.assertIn("[page.test.js:3-3](../page.test.js#L3-L3)", backend.calls[-1][0])
            self.assertIn("Unique Dependencies: `@playwright/test`", backend.calls[-1][0])
            self.assertTrue(Path(result["output"]["filepath"]).is_file())
            self.assertEqual(len(backend.calls), 8)

    def test_provided_metadata_works_with_intent_without_source_content(self):
        case = {"test_case_id": "case-1", **deepcopy(INTENT), "validation": {"passed": True},
                "context": {"suite_file": "original.ts", "line_range": [8, 10],
                            "format": "code/javascript", "imports": ["import { test } from '@playwright/test';"]}}
        metadata = case_metadata(case)
        self.assertEqual(metadata["dependencies"], ["@playwright/test"])
        self.assertEqual(metadata["source_reference"], "original.ts:8-10")
        generator = CapturingGenerator()
        BusinessLayer(generator).process(case)
        self.assertIn("Source reference: original.ts:8-10", generator.prompt)
        self.assertIn("@playwright/test", generator.prompt)

    def test_missing_metadata_is_not_inferred_from_intent_or_template(self):
        case = {"test_case_id": "case-1", **deepcopy(INTENT), "validation": {"passed": True}}
        metadata = case_metadata(case)
        self.assertEqual(metadata["dependencies"], [])
        self.assertEqual(metadata["source_reference"], "")
        self.assertEqual(metadata["line_range"], [])
        generator = CapturingGenerator()
        BusinessLayer(generator).process(case)
        self.assertNotIn("Source reference:", generator.prompt)
        self.assertIn("Unique Dependencies: None provided", generator.prompt)
        self.assertEqual(PROMPT.count("Copy source references exactly as provided."), 1)

    def test_source_urls_escape_file_names_and_do_not_invent_missing_line_numbers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "test file#1.js"
            path.write_text("test();\n")
            metadata = case_metadata({"suite": str(path), "context": {"line_range": [3, 7]}}, root / "reports")
            reference = metadata["source_reference"]
            self.assertEqual(reference, "[test file#1.js:3-7](../test%20file%231.js#L3-L7)")
            target = reference.split("](", 1)[1].split("#L", 1)[0]
            self.assertEqual((root / "reports" / unquote(target)).resolve(), path.resolve())
            without_lines = case_metadata({"suite": str(path)}, root / "reports")
            self.assertNotIn("#L", without_lines["source_reference"])
        remote = case_metadata({"source_file": "https://example.org/test.js", "line_range": [4, 6]})
        self.assertEqual(remote["source_reference"], "[test.js:4-6](https://example.org/test.js#L4-L6)")
        invalid_span = case_metadata({"source_file": "not-on-disk.js", "line_range": [9, 2]})
        self.assertEqual(invalid_span["line_range"], [])
        self.assertEqual(invalid_span["source_reference"], "not-on-disk.js")


if __name__ == "__main__":
    unittest.main()
