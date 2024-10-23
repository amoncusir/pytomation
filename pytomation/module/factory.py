import logging
from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from pytomation.module import Module

if TYPE_CHECKING:
    pass


class ModuleFactory:

    @abstractmethod
    def build(self, root_path: Path, module_path: Path) -> Module:
        raise NotImplementedError


class PythonModuleFactory(ModuleFactory):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__qualname__)

    def build(self, root_path: Path, module_path: Path) -> Module:
        pass

    def get_module_name(self, root_path: Path, module_path: Path) -> str:
        if root_path == module_path:
            return ""

        return module_path.parent.name
