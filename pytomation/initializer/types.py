from pathlib import Path
from typing import List, NewType

RootPath = NewType("RootPath", Path)
ModulesPath = NewType("ModulesPath", List[Path])
