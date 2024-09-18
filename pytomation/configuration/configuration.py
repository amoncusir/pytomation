import dataclasses
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class Configuration:
    """
    Contains properties relevant to the **execution process**.
    Like the verbosity level, the parallelization factor, the name of the modules, the module splitter (needed if
    switches the OS), the cache patterns, etc...

    Must not contain properties related to the project, like the root path, name, credentials, etc.

    The current values bay becomes from different inputs and be merged with them.
    """

    module_name: str = field(default="pytomation.py")
    module_path_splitter: str = field(default="/")
    verbosity: int = field(default=0)

    def copy(self, **changes) -> Self:
        return dataclasses.replace(self, **changes)
