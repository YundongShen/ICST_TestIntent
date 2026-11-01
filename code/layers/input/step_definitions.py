import ast
import os
from pathlib import Path
import re

KINDS = {"Given", "When", "Then", "And", "But", "Step", "defineStep"}
EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".java"}
IGNORED = {".git", ".venv", "venv", "node_modules", "__pycache__", "target", "build", "dist"}
PARAMETERS = {
    "int": r"-?\d+",
    "float": r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
    "word": r"\S+",
    "string": r'''(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')''',
    "": r".*",
}


def _expression(pattern, python=False):
    parts = []
    for part in re.split(r"(\{[^{}]*\}|\([^()]*\))", pattern):
        if part.startswith("{") and part.endswith("}"):
            name = part[1:-1]
            if python:
                kind = name.split(":", 1)[1] if ":" in name else ""
                token = {"d": PARAMETERS["int"], "g": PARAMETERS["float"],
                         "f": PARAMETERS["float"], "w": PARAMETERS["word"], "": r".+?"}.get(kind)
            else:
                token = PARAMETERS.get(name)
            if token is None:
                return None
            parts.append("(?:" + token + ")")
        elif not python and part.startswith("(") and part.endswith(")"):
            parts.append("(?:" + re.escape(part[1:-1]) + ")?")
        else:
            parts.append(re.escape(part))
    return re.compile("".join(parts))


def _mask(text):
    chars = list(text)
    i = 0
    while i < len(text):
        start = i
        if text.startswith("//", i):
            end = text.find("\n", i)
            i = len(text) if end < 0 else end
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = len(text) if end < 0 else end + 2
        elif text[i] == "/" and text[:i].rstrip()[-1:] in ("(", "=", ",", ":", "[", "!", "?", "{"):
            literal = _literal(text, i)
            if literal is None:
                i += 1
                continue
            i = literal[1]
        elif text[i] in "\"'`":
            quote = text[i]
            i += 1
            while i < len(text):
                if text[i] == "\\":
                    i += 2
                elif text[i] == quote:
                    i += 1
                    break
                else:
                    i += 1
        else:
            i += 1
            continue
        for j in range(start, min(i, len(chars))):
            if chars[j] != "\n":
                chars[j] = " "
    return "".join(chars)


def _literal(text, start):
    if start >= len(text) or text[start] not in "\"'`/":
        return None
    quote = text[start]
    end = start + 1
    in_class = False
    while end < len(text):
        char = text[end]
        if char == "\\":
            end += 2
            continue
        if quote == "/" and char == "[":
            in_class = True
        elif quote == "/" and char == "]":
            in_class = False
        elif char == quote and not in_class:
            value = text[start + 1:end]
            flags = 0
            if quote == "/":
                suffix = re.match(r"[a-z]*", text[end + 1:]).group()
                flags = re.I if "i" in suffix else 0
                end += len(suffix)
            elif quote == "`":
                if "${" in value:
                    return None
            else:
                try:
                    value = ast.literal_eval(text[start:end + 1])
                except (SyntaxError, ValueError):
                    return None
            return value, end + 1, quote == "/", flags
        end += 1
    return None


def _end(text, start, opening, closing):
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index + 1
    return None


class StepDefinitionLinker:
    def __init__(self, paths=None):
        self.paths = [paths] if isinstance(paths, (str, os.PathLike)) else paths

    def _files(self, feature):
        feature = Path(feature).resolve()
        roots = list(self.paths) if self.paths is not None else [feature.parent]
        if self.paths is None:
            for parent in feature.parents:
                if parent.name == "features":
                    roots.append(parent)
                    roots.extend(parent.parent / name for name in ("step_definitions", "steps"))
                    break
            for parent in feature.parents:
                if parent.name == "test" and parent.parent.name == "src":
                    roots.append(parent / "java")
                    break
        found = set()
        for root in roots:
            root = Path(root)
            if root.is_file():
                if root.suffix.lower() in EXTENSIONS:
                    found.add(root.resolve())
                continue
            for directory, names, files in os.walk(root):
                names[:] = sorted(name for name in names if name not in IGNORED and not name.startswith("."))
                for name in files:
                    path = Path(directory) / name
                    if path.suffix.lower() in EXTENSIONS and not path.is_symlink():
                        found.add(path.resolve())
        return sorted(found)

    def _definition(self, path, lines, start, end, kind, pattern, regex=False, flags=0, source=None):
        try:
            matcher = re.compile(pattern, flags) if regex else _expression(pattern, python=path.suffix == ".py")
        except re.error:
            return None
        if matcher is None:
            return None
        return {"path": str(path), "line_range": [start + 1, end + 1], "kind": kind.lower(),
                "pattern": pattern, "source": source if source is not None else "\n".join(lines[start:end + 1]), "matcher": matcher}

    def _python(self, path, text):
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return []
        lines = text.splitlines()
        matchers = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "use_step_matcher":
                if node.args and isinstance(node.args[0], ast.Constant):
                    matchers.append((node.lineno, node.args[0].value))
        definitions = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for decorator in node.decorator_list:
                if not isinstance(decorator, ast.Call) or not decorator.args:
                    continue
                name = decorator.func.id if isinstance(decorator.func, ast.Name) else getattr(decorator.func, "attr", "")
                if name.title() not in KINDS or not isinstance(decorator.args[0], ast.Constant):
                    continue
                pattern = decorator.args[0].value
                if not isinstance(pattern, str):
                    continue
                active = [item for item in matchers if item[0] < node.lineno]
                regex = bool(active and max(active)[1] in ("re", "re0"))
                start = min(d.lineno for d in node.decorator_list) - 1
                definition = self._definition(path, lines, start, node.end_lineno - 1, name, pattern, regex)
                if definition:
                    definitions.append(definition)
        return definitions

    def _code(self, path, text):
        lines = text.splitlines()
        masked = _mask(text)
        java = path.suffix == ".java"
        pattern = r"@(?:[\w.]+\.)?(Given|When|Then|And|But)\s*\(" if java else r"\b(Given|When|Then|And|But|defineStep)\s*\("
        definitions = []
        for match in re.finditer(pattern, masked):
            start = match.end()
            while start < len(text) and text[start].isspace():
                start += 1
            literal = _literal(text, start)
            if literal is None:
                continue
            value, end, regex, flags = literal
            if not java and not text[end:].lstrip().startswith(","):
                continue
            first = text.count("\n", 0, match.start())
            if java:
                method = masked.find("{", end)
                if method < 0:
                    continue
                stop = _end(masked, method, "{", "}")
                regex = value.startswith("^") or value.endswith("$")
            else:
                stop = _end(masked, match.end() - 1, "(", ")")
                if stop is not None and text[stop:stop + 1] == ";":
                    stop += 1
            if stop is None:
                continue
            last = text.count("\n", 0, stop - 1)
            definition = self._definition(path, lines, first, last, match.group(1), value, regex, flags,
                                          source=text[match.start():stop])
            if definition:
                definitions.append(definition)
        return definitions

    def _steps(self, source):
        steps = []
        keyword = ""
        quote = None
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith(('"""', "```")):
                marker = stripped[:3]
                quote = None if quote == marker else marker
                continue
            if quote:
                continue
            if re.match(r"(?:Scenario(?: Outline| Template)?|Background|Example)\s*:", stripped):
                keyword = ""
            match = re.match(r"(Given|When|Then|And|But|\*)\s+(.+)", stripped)
            if match:
                if match.group(1) not in ("And", "But", "*"):
                    keyword = match.group(1).lower()
                steps.append((keyword, match.group(2)))
        return steps

    def _examples(self, source):
        rows = []
        headers = None
        in_examples = False
        for line in source.splitlines():
            if re.match(r"\s*(?:Examples|Scenarios)\s*:", line):
                in_examples = True
                headers = None
            elif in_examples and line.strip().startswith("|"):
                values = [part.strip().replace(r"\|", "|") for part in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
                if headers is None:
                    headers = values
                elif len(values) == len(headers):
                    rows.append(dict(zip(headers, values)))
        return rows

    def link(self, cases, feature):
        definitions = []
        for path in self._files(feature):
            try:
                text = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError):
                continue
            definitions.extend(self._python(path, text) if path.suffix == ".py" else self._code(path, text))
        for case in cases:
            links = []
            examples = self._examples(case.source)
            for keyword, step in self._steps(case.source):
                expanded = [re.sub(r"<([^<>]+)>", lambda m: row.get(m.group(1), m.group()), step) for row in examples] if "<" in step and examples else [step]
                for definition in definitions:
                    if Path(definition["path"]).suffix == ".py" and keyword and definition["kind"] not in (keyword, "step"):
                        continue
                    matched = [text for text in expanded if definition["matcher"].fullmatch(text)]
                    if matched:
                        link = {name: value for name, value in definition.items() if name != "matcher"}
                        links.append({**link, "keyword": keyword, "step": step, "matched_text": matched})
            if links:
                case.context["step_definitions"] = links
        return cases
