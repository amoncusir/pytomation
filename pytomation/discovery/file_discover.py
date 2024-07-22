import os.path
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, List

from pytomation.discovery import Discovery
from pytomation.module import SourceFileModule
from pytomation.module_graph import MODULE_PATH_SPLITTER

if TYPE_CHECKING:
    from pytomation.module import Module


class FileDiscovery(Discovery):

    def __init__(self, cwd: PathLike, module_file_name: str):
        self.module_file_name = module_file_name
        self.cwd = cwd

    def find_modules(self) -> List['Module']:
        paths = self.find_all_modules_path()
        return [self.create_module_from_path(path) for path in paths]

    def find_all_modules_path(self) -> List[Path]:
        workdir = Path(os.path.dirname(self.cwd))
        return [path for path in workdir.rglob(self.module_file_name)]

    def get_module_name(self, path: PathLike) -> str:
        return str(path).replace(str(self.cwd), '') \
            .replace(self.module_file_name, '') \
            .strip(MODULE_PATH_SPLITTER)

    def create_module_from_path(self, path: Path) -> SourceFileModule:
        module_name = self.get_module_name(path)
        return SourceFileModule.load_from_file(module_name, path)
