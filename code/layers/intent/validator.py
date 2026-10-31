"""Compatibility interface to source-based semantic validation."""

from layers.intent.semantic_validator import SemanticValidator


class Validator:
    def __init__(self, service=None):
        self.validator = SemanticValidator(service=service)

    def validate(self, objects, goals, activities, source=""):
        report = self.validator.validate(
            {"objects": objects, "goals": goals, "activities": activities}, source)
        return {"matched": report.passed, "reasoning": "; ".join(report.issues), **report.as_dict()}

