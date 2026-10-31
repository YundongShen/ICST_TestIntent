"""Use an LLM to change description granularity while preserving verification meaning."""

import json
import math

from layers.extract.prompts import FIELDS
from layers.intent.semantic_validator import ask
from layers.json_utils import parse_json, string_list

LEVEL_WORDS = (
    (0.25, "very specific: retain the identifiers, values, paths, and calls already present"),
    (0.5, "specific: retain key identifiers, conditions, and operations"),
    (0.75, "general: describe the same verification meaning in plain terms"),
    (1.01, "very general: use broad descriptions while preserving the verification meaning"),
)


class GranularityAdjustmentError(ValueError):
    pass


def describe_level(value):
    if isinstance(value, bool):
        raise ValueError("Granularity levels must be numbers between 0 and 1")
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("Granularity levels must be numbers between 0 and 1")
    return next(text for bound, text in LEVEL_WORDS if value < bound)


ADJUST_PROMPT = """Rewrite only the requested elements of the Test Intent to match their requested level of detail.
Change description granularity, preserving the verification meaning and overall verification purpose.
Do not invent source identifiers, values, conditions, or operations.
Do not add, remove, weaken, or strengthen verification conditions or claims about what checks establish.
Keep unselected elements exactly unchanged.
{activity_rule}

[Task Requirements]
{requirements}

[Requested Levels]
{levels}

[Original Test Intent]
{intent}

Return ONLY JSON with arrays of strings for objects, goals, and activities.
"""

PRESERVATION_PROMPT = """Compare the original Test Intent and its rewritten version.
The requested description granularity may change, but verification meaning must be preserved.
Check that target coverage, verification purposes and conditions, relevant operations, and execution
order remain represented. Reject added or missing verification claims and unsupported detail.
Differences only in wording, identifier specificity, or permitted grouping are acceptable.

[Requested Levels]
{levels}
[Activity Grouping]
{activity_rule}
[Original Test Intent]
{original}
[Rewritten Test Intent]
{rewritten}

Return ONLY JSON: {{"preserved": true, "issues": []}}
Set preserved to false with short reasons if the verification meaning changed.
"""


class GranularityAdjuster:
    def __init__(self, service=None, default_levels=None, max_tokens=8000):
        self.service = service
        self.default_levels = dict(default_levels) if default_levels is not None else {
            "objects": 0.2, "goals": 0.6, "activities": 0.4}
        self.max_tokens = max_tokens

    def _service(self):
        if self.service is None:
            from model.service_factory import get_inference_backend
            self.service = get_inference_backend()
        return self.service

    def adjust(self, intent, levels=None, requirements="", merge_activities=False):
        requested = dict(self.default_levels if levels is None else levels)
        if set(requested) - set(FIELDS):
            raise ValueError("Unknown Test Intent element in granularity levels")
        descriptions = {name: describe_level(level) for name, level in requested.items()}
        original = {name: list(intent.get(name, [])) for name in FIELDS}
        if not requested:
            return dict(intent)
        activity_rule = (
            "Adjacent related activities may be grouped, preserving their order, conditions, and checks."
            if merge_activities else
            "Keep the number and order of activities unchanged; do not merge or omit activities.")
        prompt = ADJUST_PROMPT.format(
            requirements=requirements or "general documentation",
            levels=json.dumps(descriptions), activity_rule=activity_rule,
            intent=json.dumps(original, ensure_ascii=False))
        parsed = parse_json(ask(self._service(), prompt, self.max_tokens), FIELDS)
        if parsed is None:
            raise GranularityAdjustmentError("Could not read the granularity adjustment")
        rewritten = dict(original)
        for name in requested:
            values = string_list(parsed.get(name))
            if not values:
                raise GranularityAdjustmentError("Adjustment returned an empty or unreadable " + name)
            rewritten[name] = values
        if not merge_activities and len(rewritten["activities"]) != len(original["activities"]):
            raise GranularityAdjustmentError("Adjustment changed the number of activities")
        if rewritten != original:
            check_prompt = PRESERVATION_PROMPT.format(
                levels=json.dumps(descriptions), activity_rule=activity_rule,
                original=json.dumps(original, ensure_ascii=False),
                rewritten=json.dumps(rewritten, ensure_ascii=False))
            check = parse_json(ask(self._service(), check_prompt, 1500), ("preserved",)) or {}
            if check.get("preserved") is not True or string_list(check.get("issues")):
                reasons = "; ".join(string_list(check.get("issues")))
                raise GranularityAdjustmentError("Adjustment did not preserve verification meaning" +
                                                 (": " + reasons if reasons else ""))
        return {**intent, **rewritten, "granularity": {name: float(value) for name, value in requested.items()}}

