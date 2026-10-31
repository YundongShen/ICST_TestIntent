"""Compatibility interface to LLM-based granularity adjustment."""

from layers.intent.granularity_adjuster import GranularityAdjuster


class Adjuster:
    def __init__(self, service=None):
        self.adjuster = GranularityAdjuster(service=service)

    def adjust(self, objects, goals, activities, levels=None, requirements="", merge_activities=False):
        return self.adjuster.adjust(
            {"objects": objects, "goals": goals, "activities": activities},
            levels=levels, requirements=requirements, merge_activities=merge_activities)

