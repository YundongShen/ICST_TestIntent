"""Semantic validation and granularity adjustment for extracted Test Intent."""

from layers.extract import ExtractLayer
from layers.intent.granularity_adjuster import GranularityAdjuster
from layers.intent.semantic_layer import SemanticLayer, SemanticValidationError, extractor_from_layer
from layers.intent.semantic_validator import SemanticValidator


class IntentLayer:
    def __init__(self, extract_layer=None, service=None, max_reextract=2, adjust=True,
                 validator=None, adjuster=None):
        extract_layer = extract_layer if extract_layer is not None else ExtractLayer(service=service)
        self.semantic = SemanticLayer(
            extractor=extractor_from_layer(extract_layer),
            validator=validator if validator is not None else SemanticValidator(service=service),
            adjuster=adjuster if adjuster is not None else GranularityAdjuster(service=service),
            max_reextract=max_reextract, adjust=adjust)

    def process(self, extracted_data, requirements="", levels=None, merge_activities=False):
        result = self.semantic.process(
            extracted_data, source=extracted_data.get("content", ""),
            requirements=requirements, levels=levels, merge_activities=merge_activities)
        return {**extracted_data, **result}


__all__ = ["IntentLayer", "SemanticLayer", "SemanticValidator", "GranularityAdjuster", "SemanticValidationError"]

