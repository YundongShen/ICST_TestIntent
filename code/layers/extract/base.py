"""Shared inference and decoding for extraction workflows."""

from layers.extract.prompts import build_prompt
from layers.json_utils import parse_json, string_list


class ElementExtractor:
    fields = ()

    def __init__(self, service=None, max_tokens=8000):
        self.service = service
        self.max_tokens = max_tokens

    def _extract(self, source, objects=None, goals=None, feedback=""):
        if self.service is None:
            from model.service_factory import get_inference_backend
            self.service = get_inference_backend()
        prompt = build_prompt(self.fields, source, objects=objects, goals=goals, feedback=feedback)
        response = self.service.infer(prompt, max_tokens=self.max_tokens)
        data = parse_json(response, self.fields) or {}
        return {field: string_list(data.get(field)) for field in self.fields}

