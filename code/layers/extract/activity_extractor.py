"""Extract ordered Test Activities from the complete test artifact."""

from layers.extract.base import ElementExtractor


class ActivityExtractor(ElementExtractor):
    fields = ("activities",)

    def extract(self, code_text, feedback=""):
        return self._extract(code_text, feedback=feedback)
