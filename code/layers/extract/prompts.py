"""Common definitions and extraction rules for all three workflows."""

import json

FIELDS = ("objects", "goals", "activities")

RULES = {
    "objects": """[Definition: Test Objects]
Entities in the system under test whose behavior, attributes, or states are inspected,
explicitly or implicitly, through the test.

[Extraction Procedure: Test Objects]
1. Identify entities invoked during interactions with the system under test whose behavior
   is ultimately inspected. Include direct assessment and indirect assessment. If a system
   method prepares state for a later assessed invocation of another system method, both
   methods can be Test Objects.
2. Remove external drivers, testing tools, framework constructs, assertion APIs, and other
   entities that are neither part of the system under test nor subject to assessment.
   Do not exclude a system entity merely because it also participates in setup.
3. Keep specific source identifiers and distinct targets. Do not merge targets unless
   a more general representation is explicitly requested.
Output all supported Test Objects as an array of strings.""",

    "goals": """[Definition: Test Goal]
The verification purpose expressed or implied by the test artifact concerning its Test Objects.

[Extraction Procedure: Test Goal]
1. Identify the primary Test Objects. A test may involve several objects and verification conditions.
2. Use assertions, descriptions, and execution context to identify the expected behavior,
   state, or condition being verified. Distinguish stated purposes from what the implemented
   checks can establish; do not claim that a check verifies more than it actually does.
3. Describe the verification purpose clearly. Preserve distinct relevant conditions, including
   boundary or invalid-input conditions. Do not impose a fixed number of goals.
Output the supported verification purposes as an array of strings.""",

    "activities": """[Definition: Test Activities]
Operations directed toward Test Objects to trigger, observe, record, and inspect their
behaviors, attributes, and states.

[Extraction Procedure: Test Activities]
1. Identify each discrete action defined in the test, including relevant setup, execution,
   state changes, intermediate observations, and assertions.
2. Describe the semantic meaning of the actions in concise natural language and preserve
   their execution order. Preserve relevant inputs and checks.
3. Keep the specific operations separate by default. Aggregate adjacent operations only
   when a more general description is explicitly requested, preserving their verification meaning.
Output the supported Test Activities as an array of strings.""",
}


def build_prompt(fields, source, objects=None, goals=None, feedback=""):
    sections = [
        "Extract Test Intent from the supplied test artifact using the definitions and rules below.",
        "Ground each result in the complete artifact. Do not invent targets, conditions, or operations.",
    ]
    sections.extend(RULES[field] for field in fields)
    if objects is not None:
        sections += ["[Previously Extracted Objects]", json.dumps(objects, ensure_ascii=False)]
    if goals is not None:
        sections += ["[Previously Extracted Goals]", json.dumps(goals, ensure_ascii=False)]
    if feedback:
        sections += ["[Validation Feedback]", feedback, "Correct these issues using the test artifact."]
    sections += ["[Test Artifact]", source, "[Output Constraints]"]
    schema = {field: ["<supported description>"] for field in fields}
    sections += [
        "Return ONLY one JSON object with exactly these fields; every value must be an array of strings:",
        json.dumps(schema),
        "Do not output placeholders, reasoning, or markdown fences. Use an empty array if an element has no support.",
    ]
    return "\n\n".join(sections)
