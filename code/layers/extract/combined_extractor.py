"""Extract all three elements in one invocation using the common rules."""

from layers.extract.base import ElementExtractor
from layers.extract.prompts import FIELDS


class CombinedExtractor(ElementExtractor):
    fields = FIELDS

    def extract(self, code_text, feedback=""):
        return self._extract(code_text, feedback=feedback)

