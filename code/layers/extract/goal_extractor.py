"""Extract Test Goal directly from the complete test artifact."""

from layers.extract.base import ElementExtractor


class GoalExtractor(ElementExtractor):
    fields = ("goals",)

    def extract(self, code_text, feedback=""):
        return self._extract(code_text, feedback=feedback)

