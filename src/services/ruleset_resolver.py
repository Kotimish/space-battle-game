from src.interfaces.ruleset import IRuleset
from src.exceptions import ruleset as exceptions

class RulesetResolver:
    def __init__(self, rulesets: dict[str, IRuleset]):
        self._rulesets = rulesets

    def get_ruleset(self, name: str) -> IRuleset:
        if name not in self._rulesets:
            raise exceptions.RulesetNotFoundError(f"Ruleset '{name}' not found")
        return self._rulesets[name]
