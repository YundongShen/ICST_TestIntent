"""Generate an onboarding report from validated case-level Test Intent."""

from layers.business.onboarding_generator import OnboardingGenerator
from layers.business.onboarding_template import PROMPT
from layers.input.metadata import case_metadata, unique_strings


class BusinessLayer:
    def __init__(self, generator=None):
        self.generator = generator if generator is not None else OnboardingGenerator()

    def process(self, intent_data, output_dir=None):
        cases = intent_data.get("cases", [intent_data])
        if not cases:
            raise ValueError("No validated test cases were provided")
        records = []
        for case in cases:
            if case.get("validation", {}).get("passed") is not True:
                raise ValueError("Onboarding generation requires validated Test Intent")
            records.append({
                "id": case.get("test_case_id", "tc_unknown"),
                "object": "; ".join(case["objects"]),
                "goal": "; ".join(case["goals"]),
                "activities": case["activities"],
                **case_metadata(case, output_dir=output_dir),
            })
        if len({case["id"] for case in records}) != len(records):
            raise ValueError("Test case identifiers must be unique")
        suite_info = dict(intent_data.get("suite_info", {
            "suite_id": intent_data.get("suite", intent_data.get("test_case_id", "test_suite")),
            "dependencies": intent_data.get("dependencies", []),
        }))
        suite_info["dependencies"] = unique_strings(suite_info.get("dependencies"),
                                                    *(case["dependencies"] for case in records))
        grouped = self.generator.group_cases(suite_info["suite_id"], records)
        if grouped["status"] != "success":
            raise ValueError(grouped.get("error") or "Could not group the test cases")
        generated = self.generator.generate_suite_document(PROMPT, suite_info, records, grouped["groups"])
        if generated["status"] != "success" or not generated.get("document", "").strip():
            raise ValueError(generated.get("error") or "The onboarding document is empty")
        return {**intent_data, "suite_info": suite_info, "document": generated["document"], "groups": grouped["groups"]}


__all__ = ["BusinessLayer", "PROMPT"]
