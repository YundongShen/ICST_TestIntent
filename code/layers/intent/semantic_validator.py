"""Validate completeness, support from the artifact, and O/G/A consistency."""

from dataclasses import dataclass, field
import json
from typing import Dict, List

from layers.extract.prompts import FIELDS
from layers.json_utils import parse_json, string_list

_as_list = string_list


@dataclass
class ValidationReport:
    complete: bool
    supported: bool
    consistent: bool
    issues: List[str] = field(default_factory=list)
    details: Dict = field(default_factory=dict)

    @property
    def passed(self):
        return self.complete and self.supported and self.consistent

    def feedback(self):
        return "\n".join("- " + issue for issue in self.issues)

    def as_dict(self):
        return {"passed": self.passed, "complete": self.complete, "supported": self.supported,
                "consistent": self.consistent, "issues": list(self.issues)}


def ask(service, prompt, max_tokens):
    call = getattr(service, "infer_no_thinking", None) or service.infer
    return call(prompt, max_tokens=max_tokens)


SUPPORTED_PROMPT = """Check whether the extracted Test Intent is supported by the complete test artifact.
Use the code, assertions, comments, descriptions, and supporting context as evidence.
Do not infer a developer's private thoughts or undocumented original intent.
Distinguish a stated verification purpose from what the implemented checks can establish.
Reject invented entities, conditions, operations, and claims stronger than the actual checks.

[Test Artifact]
{source}

[Test Intent]
{intent}

Return ONLY JSON: {{"supported": true, "unsupported": []}}
Set supported to false and list the unsupported descriptions with short reasons when appropriate.
"""

CONSISTENT_PROMPT = """Check whether the Test Intent elements are consistent with one another:
the Test Goal concerns the Test Objects, the Test Activities operate on or assess the Test Objects,
and the Test Activities are consistent with the verification purpose and conditions of the Test Goal.
Relevant setup and intermediate checks are valid activities; do not require every setup action
to be a direct assertion.

[Test Intent]
{intent}

Return ONLY JSON: {{"consistent": true, "issues": []}}
Set consistent to false and list short reasons when appropriate.
"""


class SemanticValidator:
    def __init__(self, service=None, max_tokens=1200):
        self.service = service
        self.max_tokens = max_tokens

    def _service(self):
        if self.service is None:
            from model.service_factory import get_inference_backend
            self.service = get_inference_backend()
        return self.service

    def complete(self, intent):
        issues = []
        for name in FIELDS:
            values = intent.get(name)
            if not isinstance(values, list) or not values or not string_list(values):
                issues.append(name + " must contain readable, nonempty descriptions")
        return not issues, issues

    def supported(self, intent, source):
        prompt = SUPPORTED_PROMPT.format(source=source, intent=json.dumps(
            {name: intent.get(name, []) for name in FIELDS}, ensure_ascii=False))
        result = parse_json(ask(self._service(), prompt, self.max_tokens), ("supported",)) or {}
        ok = result.get("supported") is True
        reasons = string_list(result.get("unsupported"))
        if reasons:
            ok = False
        issues = ["not supported by the artifact: " + reason for reason in reasons]
        return ok, issues or ([] if ok else ["could not confirm support from the artifact"])

    def consistent(self, intent):
        prompt = CONSISTENT_PROMPT.format(intent=json.dumps(
            {name: intent.get(name, []) for name in FIELDS}, ensure_ascii=False))
        result = parse_json(ask(self._service(), prompt, self.max_tokens), ("consistent",)) or {}
        ok = result.get("consistent") is True
        reasons = string_list(result.get("issues"))
        if reasons:
            ok = False
        issues = ["inconsistent: " + reason for reason in reasons]
        return ok, issues or ([] if ok else ["could not confirm consistency"])

    def validate(self, intent, source):
        if not isinstance(source, str) or not source.strip():
            raise ValueError("The source artifact is required for semantic validation")
        complete, issues = self.complete(intent)
        supported = consistent = False
        if complete:
            supported, more = self.supported(intent, source)
            issues += more
            consistent, more = self.consistent(intent)
            issues += more
        return ValidationReport(complete, supported, consistent, issues)

