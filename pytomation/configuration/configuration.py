import dataclasses
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class Configuration:

    module_name: str = field(default="pytomation.py")
    module_path_splitter: str = field(default="/")
    call_path: Path = field(default_factory=Path.cwd)
    project_path: Path = field(default_factory=Path.cwd)
    verbosity: int = field(default=0)

    def copy(self, **changes) -> Self:
        return dataclasses.replace(self, **changes)
