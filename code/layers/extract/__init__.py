"""Independent, Combined, and Chained Test Intent extraction."""

from layers.extract.activity_extractor import ActivityExtractor
from layers.extract.combined_extractor import CombinedExtractor
from layers.extract.goal_extractor import GoalExtractor
from layers.extract.object_extractor import ObjectExtractor
from layers.extract.chain import ChainActivityExtractor, ChainGoalExtractor, ChainObjectExtractor


class ExtractLayer:
    def __init__(self, extract_mode="independent", service=None, max_tokens=8000):
        if extract_mode not in ("independent", "combined", "chain"):
            raise ValueError("extract_mode must be independent, combined, or chain")
        self.extract_mode = extract_mode
        options = {"service": service, "max_tokens": max_tokens}
        if extract_mode == "combined":
            self.combined_extractor = CombinedExtractor(**options)
        elif extract_mode == "chain":
            self.chain_object_extractor = ChainObjectExtractor(**options)
            self.chain_goal_extractor = ChainGoalExtractor(**options)
            self.chain_activity_extractor = ChainActivityExtractor(**options)
        else:
            self.object_extractor = ObjectExtractor(**options)
            self.goal_extractor = GoalExtractor(**options)
            self.activity_extractor = ActivityExtractor(**options)

    def process(self, preprocessed_data):
        source = preprocessed_data.get("content", "")
        if not isinstance(source, str) or not source.strip():
            raise ValueError("A nonempty test artifact is required")
        feedback = preprocessed_data.get("extraction_feedback", "")
        if self.extract_mode == "combined":
            result = self.combined_extractor.extract(source, feedback=feedback)
        elif self.extract_mode == "chain":
            objects = self.chain_object_extractor.extract(source, feedback=feedback)["objects"]
            goals = self.chain_goal_extractor.extract(source, objects=objects, feedback=feedback)["goals"]
            activities = self.chain_activity_extractor.extract(
                source, objects=objects, goals=goals, feedback=feedback)["activities"]
            result = {"objects": objects, "goals": goals, "activities": activities}
        else:
            result = {}
            for extractor in (self.object_extractor, self.goal_extractor, self.activity_extractor):
                result.update(extractor.extract(source, feedback=feedback))
        return {**preprocessed_data, **result}


__all__ = ["ExtractLayer"]
