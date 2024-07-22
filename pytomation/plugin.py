from typing import TYPE_CHECKING, Callable, Any


if TYPE_CHECKING:
    from pytomation.context import Context


class Plugin:

    name: str
    builder: Callable[['Context'], Any]

    def __init__(self, name: str, builder: Callable[['Context'], Any]):
        self.name = name
        self.builder = builder

    def build(self, context: 'Context') -> Any:
        return self.builder(context)
