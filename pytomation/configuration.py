from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Configuration:

    module_name: str = field(default="pytomation.py")
    workspace: str = field(default_factory=Path.cwd)
    verbosity: int = field(default=0)
