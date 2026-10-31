"""JSON decoding shared by extraction and semantic checks."""

import json
import re


def json_objects(text):

    if not isinstance(text, str):
        return []
    text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
    decoder = json.JSONDecoder()
    objects = []
    pos = 0
    while pos < len(text):
        start = text.find("{", pos)
        if start < 0:
            break
        try:
            value, end = decoder.raw_decode(text, start)
        except json.JSONDecodeError:
            pos = start + 1
            continue
        if isinstance(value, dict):
            objects.append(value)
        pos = end
    return objects


def parse_json(text, required=()):
    for value in reversed(json_objects(text)):
        if all(key in value for key in required):
            return value
    return None


def string_list(value):
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
        return list(value)
    return []
