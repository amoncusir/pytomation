from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from pytomation.context import Context


# TODO: Insufficient plugin management, needs a good refactor
class Plugin:

    name: str
    builder: Callable[["Context"], Any]

    def __init__(self, name: str, builder: Callable[["Context"], Any]):
        self.name = name
        self.builder = builder

    def build(self, context: "Context") -> Any:
        return self.builder(context)
