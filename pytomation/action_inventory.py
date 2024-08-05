from typing import TYPE_CHECKING, Dict, List

from _operator import itemgetter

if TYPE_CHECKING:
    from pytomation.module import Module


class ActionInventory:
    log: Dict[str, int]

    def __init__(self) -> None:
        self.log = dict()
        self._counter = 0

    def add_action(self, module: "Module", action: str, raise_error: bool) -> None:
        entry = f"{module.name}:{action}"

        if raise_error and entry in self.log.keys():
            print("\n".join(self.get_sorted_log()))
            raise ValueError(f"Duplicate log entry: {entry}. Circular dependency detected.")

        self.log[entry] = self._counter
        self._counter += 1

    def get_sorted_log(self) -> List[str]:
        return list(map(itemgetter(0), sorted(self.log.items(), key=itemgetter(1))))
