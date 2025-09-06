from pyexpat.errors import messages
from typing import Callable, Any

# todo переделать аннотацию для dependencies
class Scope:
    def __init__(self, name: str, dependencies: dict[str, Callable[[list[Any]], Any]]) -> None:
        self.name = name
        self.dependencies = dependencies
        self.parent: Scope | None = None
        self.is_default = False

    def __repr__(self) -> str:
        if self.parent:
            parent_message = self.parent.name
        else:
            parent_message = self.parent
        return f"Scope(name={self.name}, parent={parent_message}, dependencies={list(self.dependencies.keys())})"
