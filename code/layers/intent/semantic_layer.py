"""Validate, re-extract when necessary, and adjust validated Test Intent."""

from copy import deepcopy

from layers.extract.prompts import FIELDS
from layers.intent.granularity_adjuster import GranularityAdjuster
from layers.intent.semantic_validator import SemanticValidator


class SemanticValidationError(ValueError):
    def __init__(self, report, attempts):
        self.report = report
        self.attempts = attempts
        super().__init__("Test Intent failed semantic validation: " + "; ".join(report.issues))


class SemanticLayer:
    def __init__(self, extractor=None, validator=None, adjuster=None, max_reextract=2, adjust=True):
        if isinstance(max_reextract, bool) or not isinstance(max_reextract, int) or max_reextract < 0:
            raise ValueError("max_reextract must be a nonnegative integer")
        self.extractor = extractor
        self.validator = validator if validator is not None else SemanticValidator()
        self.adjuster = adjuster if adjuster is not None else GranularityAdjuster()
        self.max_reextract = max_reextract
        self.do_adjust = adjust

    def process(self, intent, source, requirements="", levels=None, merge_activities=False):
        current = deepcopy(intent)
        report = self.validator.validate(current, source)
        retries = 0
        while not report.passed and self.extractor is not None and retries < self.max_reextract:
            current = self.extractor(source, report.feedback())
            retries += 1
            report = self.validator.validate(current, source)
        if not report.passed:
            raise SemanticValidationError(report, retries)
        final = current
        if self.do_adjust:
            final = self.adjuster.adjust(current, levels=levels, requirements=requirements,
                                         merge_activities=merge_activities)
            if any(final.get(name) != current.get(name) for name in FIELDS):
                report = self.validator.validate(final, source)
                if not report.passed:
                    raise SemanticValidationError(report, retries)
        return {**final, "validation": report.as_dict(), "reextract_count": retries}


def extractor_from_layer(extract_layer):
    def run(source, feedback=""):
        result = extract_layer.process({"content": source, "extraction_feedback": feedback})
        return {name: result.get(name, []) for name in FIELDS}
    return run

