"Onboarding document generation."

import json
import re
from datetime import datetime
import os

from layers.business.goal_grouping_template import build_prompt as build_grouping_prompt


class OnboardingGenerator:


    def __init__(self, service=None):
        self.service = service

    def _service(self):
        if self.service is None:
            from model.service_factory import get_inference_backend
            self.service = get_inference_backend()
        return self.service

    def group_cases(self, suite_id, cases):


        from model.service_factory import get_inference_backend

        prompt = build_grouping_prompt(suite_id, cases)
        print("[ONBOARDING GENERATOR] Calling LLM to group test cases by shared testing question")
        service = self._service()
        raw = service.infer_no_thinking(prompt, max_tokens=1000)

        parsed = self._parse_json_object(raw)
        if parsed is None or not isinstance(parsed.get("groups"), list):
            return {"status": "error", "groups": [], "error": "could not parse grouping JSON"}
        all_ids = {case["id"] for case in cases}
        seen = []
        for group in parsed["groups"]:
            if not isinstance(group, dict) or not isinstance(group.get("shared_question"), str) or not group["shared_question"].strip():
                return {"status": "error", "groups": [], "error": "invalid group description"}
            ids = group.get("test_case_ids")
            if not isinstance(ids, list) or not ids or not all(isinstance(cid, str) for cid in ids):
                return {"status": "error", "groups": [], "error": "invalid group case identifiers"}
            seen.extend(ids)
        if set(seen) != all_ids or len(seen) != len(all_ids):
            return {"status": "error", "groups": [], "error": "grouping must include every case exactly once"}

        return {"status": "success", "groups": parsed["groups"], "error": None}

    @staticmethod
    def _parse_json_object(text):


        from layers.json_utils import parse_json
        return parse_json(text, ("groups",))

    def generate_suite_document(self, prompt_template, suite_info, cases, groups):


        prompt = self._build_suite_prompt(prompt_template, suite_info, cases, groups)
        print("[ONBOARDING GENERATOR] Calling LLM to generate suite-level document")
        return self._generate_with_model(prompt, marker="## Test Suite Overview", use_thinking=False)

    @staticmethod
    def _build_suite_prompt(format_guide, suite_info, cases, groups):
        by_id = {c["id"]: c for c in cases}

        cases_desc = []
        for c in cases:
            deps = ", ".join(f"`{d}`" for d in c.get("dependencies", []))
            cases_desc.append(f"- {c['id']} (dependencies: {deps})")
        cases_block = "\n".join(cases_desc)

        groups_desc = []
        for gi, g in enumerate(groups, 1):
            groups_desc.append(f"Group {gi}: {', '.join(g['test_case_ids'])}")
            groups_desc.append(f"Shared testing question: {g['shared_question']}")
            for cid in g["test_case_ids"]:
                c = by_id.get(cid)
                if not c:
                    continue
                acts = "\n".join(f"  - {a}" for a in c.get("activities", []))
                groups_desc.append(
                    f"  [{cid}]\n"
                    f"  Object: {c['object']}\n"
                    f"  Goal: {c['goal']}\n"
                    f"  Activities:\n{acts}"
                )
            groups_desc.append("")
        groups_block = "\n".join(groups_desc)

        deps_str = ", ".join(f"`{d}`" for d in suite_info.get("dependencies", []))

        return f"""{format_guide}

【Suite Info】
Suite ID: {suite_info['suite_id']}
Test cases: {len(cases)}
Suite description: {suite_info.get('description', '')}
Unique Dependencies: {deps_str}

【Test Cases (in order)】
{cases_block}

【Groups (already decided, do not re-group)】
{groups_block}

Based on the above content and format requirements, generate the Onboarding document:"""

    def generate(self, prompt_template, objects, goals, activities):

        prompt = self._build_prompt(prompt_template, objects, goals, activities)

        print("[ONBOARDING GENERATOR] Calling LLM to generate")
        return self._generate_with_model(prompt)

    def _generate_with_model(self, prompt, marker="# Test Intent-Driven Onboarding Document", use_thinking=True):

        from model.service_factory import get_inference_backend

        service = self._service()
        if use_thinking:
            document = service.infer(prompt, max_tokens=8000)
        else:
            document = service.infer_no_thinking(prompt, max_tokens=8000)


        if marker in document:
            document = document[document.rindex(marker):]

        if not document.strip():
            return {"status": "error", "document": "", "error": "Model returned an empty document"}
        print("[ONBOARDING GENERATOR] Generation completed")
        return {"status": "success", "document": document, "error": None}

    def _build_prompt(self, format_guide, objects, goals, activities):


        objects_str = "\n".join([f"- {obj}" for obj in objects])
        goals_str = "\n".join([f"- {goal}" for goal in goals])
        activities_str = "\n".join([f"- {activity}" for activity in activities])

        return f"""{format_guide}

【Test Intent Content to Generate】
Objects:
{objects_str}

Goals:
{goals_str}

Activities:
{activities_str}

Based on the above content and format requirements, generate Onboarding document:"""

    def save_document(self, document):

        try:

            result_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "onboarding_result")
            os.makedirs(result_dir, exist_ok=True)


            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"onboarding_{timestamp}.md"
            output_path = os.path.join(result_dir, filename)


            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(document)

            print(f"[ONBOARDING GENERATOR] Document saved to: {output_path}")

            return {
                "status": "success",
                "path": output_path,
                "error": None
            }
        except Exception as e:
            print(f"[ONBOARDING GENERATOR] Save failed: {e}")
            return {
                "status": "error",
                "path": "",
                "error": str(e)
            }
