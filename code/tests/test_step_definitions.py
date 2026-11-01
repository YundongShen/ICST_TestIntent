from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from layers.extract import ExtractLayer
from layers.input.normalizer import Normalizer
from layers.input.pipeline import InputPipeline
from tests.test_extraction_pipeline import Backend, extraction_responses


class StepDefinitionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_javascript_links_only_matching_background_and_scenario_steps(self):
        path = self.write("features/account.feature", """Feature: Accounts
  Background:
    Given an initialized account
  Scenario: read
    When I choose 3 messages
    Then I see "ready"
  Scenario: reset
    When I reset the account
""")
        definitions = self.write("features/step_definitions/account.ts", """import { Given, When, Then } from '@cucumber/cucumber';
throw new Error('step files must not execute');
Given('an initialized account', () => {
  initialize();
});
When('I choose {int} message(s)', async (count) => {
  await choose(count);
});
Then('I see {string}', (value) => {
  expect(read()).toBe(value);
});
When('I reset the account', () => {
  reset();
});
// Given('an initialized account', () => { fakeComment(); });
const text = "Given('an initialized account', () => { fakeString(); })";
""")
        self.write("features/node_modules/fake.js", "Given('an initialized account', () => { fakeDependency(); });")
        cases = InputPipeline().run(str(path))
        self.assertEqual([case.case_id for case in cases], ["account_1", "account_2"])
        first, second = InputPipeline.as_records(cases)
        self.assertEqual(len(cases[0].context["step_definitions"]), 3)
        self.assertEqual(len(cases[1].context["step_definitions"]), 2)
        self.assertIn("initialize();", first["content"])
        self.assertIn("await choose(count);", first["content"])
        self.assertNotIn("reset();", first["content"])
        self.assertIn("reset();", second["content"])
        self.assertNotIn("await choose(count);", second["content"])
        self.assertNotIn("fake", first["content"])
        self.assertNotIn("throw new Error", first["content"])
        self.assertTrue(first["content"].startswith(cases[0].source))
        self.assertNotIn("initialize();", cases[0].source)
        for definition in cases[0].context["step_definitions"]:
            self.assertEqual(definition["path"], str(definitions.resolve()))
            start, end = definition["line_range"]
            self.assertEqual(definition["source"], "\n".join(definitions.read_text().splitlines()[start - 1:end]))

    def test_outline_expands_examples_and_deduplicates_definition_source(self):
        source = '''Feature: Scores
  Scenario Outline: choose a score
    Given I choose <value>
    And I choose <value>
    Then the message is
      """
      Given a docstring must not become a step
      """
    Examples:
      | value |
      | 12    |
      | 23    |
'''
        path = self.write("features/scores.feature", source)
        self.write("features/steps/scores.js", '''const { Given } = require('@cucumber/cucumber');
Given(/^I choose (\\d+)$/i, (number) => {
  choose(number);
});
Given('a docstring must not become a step', () => {
  forbidden();
});
''')
        case = InputPipeline().run(str(path))[0]
        links = case.context["step_definitions"]
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]["matched_text"], ["I choose 12", "I choose 23"])
        content = InputPipeline.as_records([case])[0]["content"]
        self.assertEqual(content.count("choose(number);"), 1)
        self.assertNotIn("forbidden();", content)
        self.assertEqual(case.source, source)

    def test_python_parse_steps_respect_keyword_and_explicit_definition_paths(self):
        path = self.write("specs/login.feature", """Feature: Login
  Scenario: log in
    Given I have 2 accounts
    And I have 3 accounts
    When I log in as alice
""")
        definitions = self.write("support/steps.py", """from behave import given, when
import missing_project_dependency

@given('I have {count:d} accounts')
def prepare(context, count):
    context.accounts = count

@when('I have {count:d} accounts')
def wrong_keyword(context, count):
    wrong_branch()

@when('I log in as {name}')
def login(context, name):
    context.login(name)
""")
        pipeline = InputPipeline(Normalizer(step_definition_paths=definitions))
        case = pipeline.run(str(path))[0]
        links = case.context["step_definitions"]
        self.assertEqual(len(links), 3)
        content = pipeline.as_records([case])[0]["content"]
        self.assertIn("context.accounts = count", content)
        self.assertIn("context.login(name)", content)
        self.assertNotIn("wrong_branch()", content)
        self.assertEqual(content.count("def prepare"), 1)

    def test_python_regex_step_matcher(self):
        path = self.write("features/state.feature", "Feature: State\n  Scenario: read\n    Then the value is 7\n")
        self.write("features/steps/state.py", """from behave import then, use_step_matcher
use_step_matcher('re')

@then(r'the value is (?P<value>\\d+)')
def read(context, value):
    assert context.value == int(value)
""")
        case = InputPipeline().run(str(path))[0]
        self.assertIn("assert context.value", case.context["step_definitions"][0]["source"])

    def test_java_steps_are_found_in_conventional_test_source_directory(self):
        path = self.write("src/test/resources/features/page.feature", "Feature: Page\n  Scenario: open\n    Given the page is open\n    Then the count is 4\n")
        self.write("src/test/java/example/PageSteps.java", """package example;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
public class PageSteps {
    @Given("the page is open")
    public void open() {
        page.open();
    }
    @Then("^the count is (\\\\d+)$")
    public void count(int expected) {
        assertEquals(expected, page.count());
    }
}
""")
        case = InputPipeline().run(str(path))[0]
        self.assertEqual(len(case.context["step_definitions"]), 2)
        content = InputPipeline.as_records([case])[0]["content"]
        self.assertIn("page.open();", content)
        self.assertIn("assertEquals(expected, page.count());", content)

    def test_ambiguous_matches_are_kept_without_choosing_an_implementation(self):
        path = self.write("features/read.feature", "Feature: Read\n  Scenario: read\n    Given the page is open\n")
        for name in ("one", "two"):
            self.write(f"features/steps/{name}.js", f"Given('the page is open', () => {{ {name}(); }});\n")
        links = InputPipeline().run(str(path))[0].context["step_definitions"]
        self.assertEqual(len(links), 2)
        self.assertNotEqual(links[0]["path"], links[1]["path"])

    def test_shared_registration_lines_do_not_include_unmatched_definitions(self):
        path = self.write("features/page.feature", "Feature: Page\n  Scenario: read\n    Given the page is open\n")
        self.write("features/steps/page.js", """const { Given } = require('@cucumber/cucumber'); Given('the page is open', () => {
  actualCheck();
}); Given('an unrelated step', () => { unrelated(); });
""")
        record = InputPipeline.as_records(InputPipeline().run(str(path)))[0]
        self.assertIn("actualCheck();", record["content"])
        self.assertNotIn("unrelated();", record["content"])
        self.assertNotIn("require('@cucumber/cucumber')", record["content"])

    def test_matching_definitions_on_the_same_line_are_both_passed_to_extraction(self):
        path = self.write("features/page.feature", "Feature: Page\n  Scenario: read\n    Given the page is open\n    When I read the page\n")
        self.write("features/steps/page.js", "Given('the page is open', () => { openPage(); }); When('I read the page', () => { readPage(); });\n")
        record = InputPipeline.as_records(InputPipeline().run(str(path)))[0]
        self.assertIn("openPage();", record["content"])
        self.assertIn("readPage();", record["content"])

    def test_absent_or_unmatched_definitions_preserve_source_and_record_shape(self):
        source = "Feature: Read\r\n  Scenario: read\r\n    Given an unknown step\r\n"
        path = self.write("features/read.feature", source)
        self.write("features/steps/bad.js", "Given(/[/, () => {});\nGiven('an unrelated step', () => {});\n")
        self.write("features/steps/bad.py", "not valid Python !!!")
        case = InputPipeline().run(str(path))[0]
        self.assertEqual(case.source, source)
        self.assertNotIn("step_definitions", case.context)
        record = InputPipeline.as_records([case])[0]
        self.assertEqual(record["content"], source)
        self.assertEqual(set(record), {"content", "test_case_id", "title", "suite", "context"})

    def test_non_gherkin_and_disabled_linking_do_not_scan_definitions(self):
        js = self.write("one.test.js", "test('one', () => { expect(1).toBe(1); });\n")
        feature = self.write("read.feature", "Feature: Read\n  Scenario: read\n    Given the page is open\n")
        with patch("layers.input.step_definitions.StepDefinitionLinker._files", side_effect=AssertionError("Unexpected scan")):
            case = InputPipeline().run(str(js))[0]
            self.assertEqual(InputPipeline.as_records([case])[0]["content"], js.read_text())
            disabled = InputPipeline(Normalizer(link_context=False)).run(str(feature))[0]
            self.assertEqual(disabled.context, {})
            self.assertEqual(InputPipeline.as_records([disabled])[0]["content"], feature.read_text())

    def test_all_extraction_workflows_receive_linked_source_without_extra_inference(self):
        path = self.write("features/read.feature", "Feature: Read\n  Scenario: read\n    Given the page is open\n")
        self.write("features/steps/page.js", "Given('the page is open', () => { actualCheck(); });\n")
        record = InputPipeline.as_records(InputPipeline().run(str(path)))[0]
        for mode in ("independent", "combined", "chain"):
            with self.subTest(mode=mode):
                backend = Backend(extraction_responses(mode))
                result = ExtractLayer(mode, service=backend).process(record)
                self.assertEqual(len(backend.calls), 1 if mode == "combined" else 3)
                self.assertTrue(all("actualCheck();" in prompt for prompt, _ in backend.calls))
                self.assertIn("objects", result)


if __name__ == "__main__":
    unittest.main()
