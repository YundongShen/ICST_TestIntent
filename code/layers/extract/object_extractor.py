"""Extract Test Objects directly from the complete test artifact."""

from layers.extract.base import ElementExtractor


class ObjectExtractor(ElementExtractor):
    fields = ("objects",)

    def extract(self, code_text, feedback=""):
        return self._extract(code_text, feedback=feedback)
