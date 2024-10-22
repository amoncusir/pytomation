import logging
import os
import os.path
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, List

from old.discovery import Discovery
from pytomation.module import SourceFileModule

if TYPE_CHECKING:
    from pytomation.module import Module


class FileDiscovery(Discovery):

    def __init__(self, workdir: PathLike, module_file_name: str):

        self.module_file_name = module_file_name
        self.workdir = Path(workdir)

    def find_modules(self) -> List["Module"]:
        paths = self.find_all_modules_path()
        return [self.create_module_from_path(path) for path in paths]

    def find_all_modules_path(self) -> List[Path]:
        logging.debug(f"Finding all modules in {self.workdir} like {self.module_file_name}")

        modules_path_list = [path for path in self.workdir.rglob(self.module_file_name)]

        logging.debug(f"Found {len(modules_path_list)} modules in {self.workdir} :: %s", modules_path_list)

        return modules_path_list

    def get_module_name(self, path: PathLike) -> str:
        return str(path).replace(str(self.workdir), "").replace(self.module_file_name, "").strip(os.sep)

    def create_module_from_path(self, path: Path) -> SourceFileModule:
        module_name = self.get_module_name(path)
        return SourceFileModule.load_from_file(module_name, path)
