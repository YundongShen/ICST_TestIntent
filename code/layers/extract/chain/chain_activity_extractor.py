"""Third chained stage: extract activities with Objects and Goal as context."""

from layers.extract.activity_extractor import ActivityExtractor


class ChainActivityExtractor(ActivityExtractor):
    def extract(self, code_text, objects=None, goals=None, feedback=""):
        return self._extract(code_text, objects=objects, goals=goals, feedback=feedback)
