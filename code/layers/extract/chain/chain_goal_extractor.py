"""Second chained stage: extract Test Goal with Test Objects as context."""

from layers.extract.goal_extractor import GoalExtractor


class ChainGoalExtractor(GoalExtractor):
    def extract(self, code_text, objects=None, feedback=""):
        return self._extract(code_text, objects=objects, feedback=feedback)
