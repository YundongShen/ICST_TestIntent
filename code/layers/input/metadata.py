import ast
import os
from pathlib import Path
import re
from urllib.parse import quote, urldefrag, urlsplit

from layers.input.step_definitions import _literal, _mask


def unique_strings(*values):
    result = []
    for items in values:
        if not isinstance(items, (list, tuple)):
            continue
        for value in items:
            if isinstance(value, str) and value.strip() and value not in result:
                result.append(value)
    return result


def _skip(source, position):
    pattern = re.compile(r"\s+|//[^\n]*|/\*[\s\S]*?\*/")
    while True:
        match = pattern.match(source, position)
        if not match:
            return position
        position = match.end()


def _module(source, position):
    position = _skip(source, position)
    if source[position:position + 1] not in ("'", '"'):
        return None
    literal = _literal(source, position)
    return literal[0] if literal else None


def declared_dependencies(source, format):
    if format == "code/python":
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []
        names = []
        nodes = sorted((node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))),
                       key=lambda node: (node.lineno, node.col_offset))
        for node in nodes:
            if isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names.append("." * node.level + node.module)
                else:
                    names.extend("." * node.level + alias.name for alias in node.names)
        return unique_strings(names)
    if format not in ("code/javascript", "code/java"):
        return []
    masked = _mask(source)
    names = []
    if format == "code/java":
        for match in re.finditer(r"\bimport\s+(?:static\s+)?([\w.*]+)\s*;", masked):
            names.append(match.group(1))
    else:
        statements = list(re.finditer(r"\b(import|export|require)\b", masked))
        for index, match in enumerate(statements):
            position = _skip(source, match.end())
            name = None
            if match.group() == "require" or source[position:position + 1] == "(":
                if source[position:position + 1] == "(":
                    name = _module(source, position + 1)
            elif match.group() == "import" and source[position:position + 1] in ("'", '"'):
                name = _module(source, position)
            else:
                limit = statements[index + 1].start() if index + 1 < len(statements) else len(masked)
                semicolon = masked.find(";", position, limit)
                if semicolon >= 0:
                    limit = semicolon
                from_token = re.search(r"\bfrom\b", masked[position:limit])
                if from_token:
                    name = _module(source, position + from_token.end())
            if name:
                names.append(name)
    return unique_strings(names)


def case_metadata(case, output_dir=None):
    context = case.get("context") or {}
    dependencies = unique_strings(case.get("dependencies"), context.get("dependencies"))
    if not dependencies and context.get("imports"):
        dependencies = declared_dependencies("\n".join(unique_strings(context["imports"])), context.get("format"))
    source = case.get("source_file") or case.get("file_path") or context.get("source_file") or case.get("suite") or context.get("suite_file") or case.get("file_name")
    span = case.get("line_range") or context.get("line_range")
    if not (isinstance(span, (list, tuple)) and len(span) == 2
            and all(type(value) is int for value in span) and 0 < span[0] <= span[1]):
        span = []
    reference = case.get("source_reference", "")
    if source and not reference:
        source = os.fspath(source)
        remote = urlsplit(source).scheme in ("http", "https")
        name = urlsplit(source).path.rsplit("/", 1)[-1] if remote else source.replace("\\", "/").rsplit("/", 1)[-1]
        label = name.replace("[", r"\[").replace("]", r"\]")
        target = ""
        if remote:
            target = urldefrag(source)[0]
        elif Path(source).is_file():
            target = quote(Path(os.path.relpath(Path(source).resolve(), Path(output_dir or ".").resolve())).as_posix(), safe="/")
        if span:
            label += f":{span[0]}-{span[1]}"
            if target:
                target += f"#L{span[0]}-L{span[1]}"
        reference = f"[{label}]({target})" if target else label
    return {"dependencies": dependencies, "source_file": os.fspath(source) if source else "",
            "line_range": list(span), "source_reference": reference}
