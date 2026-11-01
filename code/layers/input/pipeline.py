from typing import Iterable, List

from layers.input.adapters import parse_suite
from layers.input.normalizer import Normalizer, TestCase


class InputPipeline:
    def __init__(self, normalizer=None):
        self.normalizer = normalizer or Normalizer()

    def run(self, path) -> List[TestCase]:
        return self.normalizer.run(parse_suite(path))

    def run_many(self, paths: Iterable[str]) -> List[TestCase]:
        cases = []
        for path in paths:
            cases.extend(self.run(path))
        return cases

    @staticmethod
    def as_records(cases: List[TestCase]):
        records = []
        for case in cases:
            content = case.source
            if case.format == "gherkin":
                definitions = {}
                for definition in case.context.get("step_definitions", []):
                    key = (definition["path"], tuple(definition["line_range"]), definition["source"])
                    definitions[key] = definition["source"]
                if definitions:
                    content += ("\n" if content.endswith(("\n", "\r")) else "\n\n") + "\n\n".join(definitions.values()) + "\n"
            records.append({"content": content, "test_case_id": case.case_id, "title": case.title,
                            "suite": case.suite, "context": case.context})
        return records
