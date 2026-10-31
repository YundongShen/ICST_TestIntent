"""Shared processing for the onboarding test versions."""

from copy import deepcopy
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TEST_OUTPUT = ROOT / "Result" / "onboarding_test"
CASE_DIR = TEST_OUTPUT / "case_extractions"
FIELDS = ("objects", "goals", "activities")


def test_service():
    from model.service_factory import get_inference_backend
    os.environ.setdefault("INFERENCE_BACKEND", "local")
    os.environ.setdefault("MODEL_TYPE", "qwen")
    if os.environ["INFERENCE_BACKEND"] == "local":
        from model import inference_service
        if inference_service._model_config is None:
            if os.environ["MODEL_TYPE"] == "qwen":
                from model.model_config_qwen import MODEL_CONFIG
            elif os.environ["MODEL_TYPE"] in ("7b", "deepseek"):
                from model.model_config_7b import MODEL_CONFIG
            else:
                raise ValueError("MODEL_TYPE must be qwen, deepseek, or 7b")
            inference_service.set_model_config(MODEL_CONFIG)
    return get_inference_backend()


def case_id(suite, index):
    return f"TC-{suite['suite_id'].split('-')[0]}-{index:02d}"


def triplet(record):
    intent = {field: deepcopy(record.get(field)) for field in FIELDS}
    for field, values in intent.items():
        if not isinstance(values, list) or not values or not all(
                isinstance(value, str) and value.strip() for value in values):
            raise ValueError(f"{field} must contain nonempty descriptions")
    return intent


def validate_record(record, service):
    from layers.intent.semantic_validator import SemanticValidator
    source = record.get("source", "")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("The source artifact is missing; regenerate this test-version extraction")
    intent = triplet(record)
    report = SemanticValidator(service=service).validate(intent, source)
    if not report.passed:
        raise ValueError("Semantic validation failed: " + "; ".join(report.issues))
    return report


def extract_validate_adjust(source, service, extract_layer=None, max_reextract=2):
    from layers import ExtractLayer
    from layers.intent.granularity_adjuster import GranularityAdjuster
    from layers.intent.semantic_layer import SemanticLayer
    from layers.intent.semantic_validator import SemanticValidator, ask, parse_json
    if not isinstance(max_reextract, int) or isinstance(max_reextract, bool) or max_reextract < 0:
        raise ValueError("max_reextract must be a nonnegative integer")
    extraction = extract_layer if extract_layer is not None else ExtractLayer(extract_mode="independent")

    def extract_again(content, feedback=""):

        return extraction.process({"content": content, "extraction_feedback": feedback})

    semantic = SemanticLayer(
        extractor=extract_again, validator=SemanticValidator(service=service),
        max_reextract=max_reextract, adjust=False)
    initial = extract_again(source)
    validated = semantic.process(initial, source=source)
    if validated.get("validation", {}).get("passed") is not True:
        raise ValueError("Semantic validation failed after the extraction retries")
    original = triplet(validated)
    adjusted = GranularityAdjuster(service=service).adjust(
        deepcopy(original), levels={"objects": 0.2, "goals": 0.6, "activities": 0.4},
        requirements="Test onboarding: preserve verification meaning and the actual strength of checks.")
    rewritten = triplet(adjusted)
    if rewritten != original:
        prompt = (
            "Check whether the rewritten Test Intent preserves the verification meaning of the original. "
            "Granularity may change, but target coverage, verification conditions, operations, and their order "
            "must remain represented. Do not accept a stated aim being changed into a stronger claim about "
            "what an implemented check verifies.\n"
            "[Original Test Intent]\n" + json.dumps(original, ensure_ascii=False) +
            "\n[Rewritten Test Intent]\n" + json.dumps(rewritten, ensure_ascii=False) +
            '\nReturn ONLY JSON: {"preserved": true/false, "issues": ["short reason"]}')
        check = parse_json(ask(service, prompt, 1500)) or {}
        if check.get("preserved") is not True or check.get("issues"):
            raise ValueError("Granularity adjustment changed or did not confirm verification meaning")
    final_record = {**adjusted, "source": source}
    report = validate_record(final_record, service)
    return {**final_record, "validation": {
        "passed": report.passed, "complete": report.complete, "supported": report.supported,
        "consistent": report.consistent, "issues": report.issues},
        "reextract_count": validated.get("reextract_count", 0)}


def document_case(record):
    intent = triplet(record)
    return {
        "id": record["case_id"], "object": "; ".join(intent["objects"]),
        "goal": "; ".join(intent["goals"]), "activities": intent["activities"],
        "dependencies": record.get("dependencies", []),
    }


def generate_document(suite, cases, service, out_path):
    from layers.business.onboarding_generator import OnboardingGenerator
    from layers.business.onboarding_template import PROMPT
    generator = OnboardingGenerator()
    if hasattr(generator, "service"):
        generator.service = service
    groups = generator.group_cases(suite["suite_id"], cases)
    if groups["status"] != "success":
        raise ValueError(groups.get("error") or "Test-case grouping failed")
    ids = [cid for group in groups["groups"] for cid in group.get("test_case_ids", [])]
    expected = [case["id"] for case in cases]
    if len(ids) != len(expected) or set(ids) != set(expected):
        raise ValueError("Grouping must include each supplied case exactly once")
    info = {key: suite[key] for key in ("suite_id", "description", "dependencies")}
    generated = generator.generate_suite_document(PROMPT, info, cases, groups["groups"])
    if generated["status"] != "success" or not generated.get("document", "").strip():
        raise ValueError(generated.get("error") or "Document generation returned empty text")
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(generated["document"], encoding="utf-8")
    return target


def default_groundtruth_dir():
    configured = os.getenv("GROUNDTRUTH_DIR")
    if configured:
        return Path(configured)
    candidates = (ROOT / "Data" / "Groundtruth",
                  ROOT.parent / "ICST_TestIntent" / "Data" / "Groundtruth")
    return next((path for path in candidates if path.is_dir()), candidates[-1])


def read_groundtruth(path):
    sections = {}
    current = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        heading = re.fullmatch(r"\s*\*\*Test (Objects?|Goals?|Activities)\*\*\s*", line)
        if heading:
            word = heading.group(1).lower()
            current = "objects" if word.startswith("object") else "goals" if word.startswith("goal") else "activities"
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    result = {}
    for field in ("objects", "goals"):
        text = "\n".join(sections.get(field, [])).strip()
        result[field] = [text] if text else []
    activities = []
    for line in sections.get("activities", []):
        if not line.strip():
            continue
        step = re.match(r"\s*\d+[.)]\s+(.*)", line)
        if step:
            activities.append(step.group(1))
        elif activities:
            activities[-1] += "\n" + line.strip()
        else:
            raise ValueError("Unrecognized activity format in " + str(path))
    result["activities"] = activities
    return triplet(result)


def load_groundtruth_cases(suite, directory):
    stem = Path(suite["source_file"]).stem
    cases = []
    for index in range(1, len(suite["cases"]) + 1):
        path = Path(directory) / suite["framework"] / f"{stem}_{index}.txt"
        intent = read_groundtruth(path)
        cases.append(document_case({
            **intent, "case_id": case_id(suite, index), "dependencies": suite["dependencies"]}))
    return cases
