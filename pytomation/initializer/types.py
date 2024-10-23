from pathlib import Path
from typing import Dict, List, NewType

from pytomation.module import Module

RootPath = NewType("RootPath", Path)
ModulesPath = NewType("ModulesPath", List[Path])
ModuleTree = NewType("ModuleTree", Dict[str, Module])
