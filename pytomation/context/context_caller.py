from dataclasses import dataclass, field
from typing import NewType, Tuple

from pytomation.module import Module
from pytomation.module.action import Action

ItemArg = Tuple[str, ...] | str


@dataclass(frozen=True)
class ContextCaller:
    module: Module
    action: Action
    arguments: Tuple[str, ...] = field(default_factory=tuple)

    @property
    def has_arguments(self) -> bool:
        return len(self.arguments) > 0

    def __contains__(self, item: ItemArg) -> bool:
        if isinstance(item, str):
            return item in self.arguments

        for value in item:
            if value in self.arguments:
                return True
        return False

    def argument_index(self, item: ItemArg) -> int:
        if isinstance(item, str):
            return self.arguments.index(item)

        for value in item:
            try:
                return self.arguments.index(value)
            except ValueError:
                pass
        raise ValueError

    def __getitem__(self, item: ItemArg) -> Tuple[str, ...]:
        index = self.argument_index(item) + 1
        iterable = iter(self.arguments[index:])
        values = []

        for value in iterable:
            if value.startswith("-"):
                return tuple(values)

            values.append(value)

        return tuple(values)
