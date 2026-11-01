from pathlib import Path
import tempfile
import unittest

from layers.input.pipeline import InputPipeline


class SplittingTests(unittest.TestCase):
    def split(self, name, source):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / name
            path.write_bytes(source.encode())
            return InputPipeline().run(str(path))

    def test_single_case_preserves_original_bytes(self):
        source = "// Shared context\r\nconst seed = 1;\r\ntest('one', () => { expect(seed).toBe(1); });\r\n"
        cases = self.split("one.test.js", source)
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0].case_id, "one.test")
        self.assertEqual(cases[0].source, source)

    def test_nested_groups_keep_only_applicable_setup_metadata(self):
        source = """import helper from './helper';
beforeAll(() => { helper.connect(); });
describe('outer', () => {
  beforeEach(() => { helper.reset(); });
  describe('left', () => {
    beforeEach(() => { helper.left(); });
    test('one', () => { expect(helper.read()).toBe(1); });
  });
  describe('right', () => {
    beforeEach(() => { helper.right(); });
    test('two', () => { expect(helper.read()).toBe(2); });
  });
});
"""
        cases = self.split("nested.test.js", source)
        self.assertEqual([c.title for c in cases], ["one", "two"])
        for case, own, sibling in [(cases[0], "left", "right"), (cases[1], "right", "left")]:
            self.assertIn("import helper", case.source)
            setup = "\n".join(case.context["shared_setup"])
            for call in ["connect", "reset", own]:
                self.assertIn("helper." + call + "()", case.source)
                self.assertIn("helper." + call + "()", setup)
            self.assertNotIn("helper." + sibling + "()", case.source)
            self.assertNotIn("helper." + sibling + "()", setup)

    def test_python_checks_using_empty_dicts_are_not_removed(self):
        source = """def test_first():
    assert make_first() == {}

def test_second():
    assert make_second() == {}
"""
        cases = self.split("test_dicts.py", source)
        self.assertEqual([c.title for c in cases], ["test_first", "test_second"])
        self.assertIn("make_first", cases[0].source)
        self.assertNotIn("make_second", cases[0].source)
        self.assertIn("make_second", cases[1].source)
        self.assertNotIn("make_first", cases[1].source)

    def test_gherkin_keeps_tags_background_and_scenario_examples(self):
        source = """@suite
Feature: Shared state
  Background:
    Given an initialized account

  @one
  Scenario Outline: first
    When I choose <value>
    Then the result is <value>
    Examples:
      | value |
      | 1     |

  @two
  Scenario: second
    Then I see the account
"""
        cases = self.split("state.feature", source)
        self.assertEqual(len(cases), 2)
        for case in cases:
            self.assertIn("@suite", case.source)
            self.assertIn("Given an initialized account", case.source)
        self.assertIn("@one", cases[0].source)
        self.assertIn("| 1     |", cases[0].source)
        self.assertNotIn("@two", cases[0].source)
        self.assertIn("@two", cases[1].source)
        self.assertNotIn("@one", cases[1].source)


if __name__ == "__main__":
    unittest.main()
