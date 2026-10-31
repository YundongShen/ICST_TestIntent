"""Preserve the text and verification evidence of a test artifact."""

from pathlib import Path


class Preprocessor:
    def process(self, raw_code):
        if not isinstance(raw_code, str):
            raise TypeError("Test artifact content must be text")

        return raw_code

    def process_file(self, file_path):
        path = Path(file_path)
        with path.open(encoding="utf-8", newline="") as source:
            content = source.read()
        return {"content": self.process(content), "file_name": path.name, "file_path": str(path)}

    @staticmethod
    def validate(cleaned_data):
        return isinstance(cleaned_data, dict) and isinstance(cleaned_data.get("content"), str) and bool(cleaned_data["content"].strip())
