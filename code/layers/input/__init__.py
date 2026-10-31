"""Input processing that preserves the evidence in a test artifact."""

from layers.input.preprocessor import Preprocessor
from layers.input.pipeline import InputPipeline


class InputLayer:
    def __init__(self):
        self.preprocessor = Preprocessor()

    def process(self, raw_data):
        return {**raw_data, "content": self.preprocessor.process(raw_data.get("content", ""))}


__all__ = ["InputLayer", "InputPipeline"]
