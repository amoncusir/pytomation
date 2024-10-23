import logging
from pathlib import Path
from typing import Callable, List

from pytomation.configuration import Configuration
from pytomation.initializer.initializer import InitializationChain
from pytomation.initializer.types import ModulesPath, RootPath
from pytomation.utils.store import TypedStore


class ModuleFinderChain(InitializationChain):

    def __init__(self, order=0):
        super().__init__(order)
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, next_handler: Callable[[TypedStore], TypedStore], context: TypedStore) -> TypedStore:

        config = context.get(Configuration)
        workdir = context.get(RootPath)
        module_name = config.module_name

        modules = context.get(ModulesPath, [])
        modules.extend(self.find_modules(workdir, module_name))
        context.put(modules, type_value=ModulesPath)

        return next_handler(context)

    def find_modules(self, workdir: Path, module_name: str) -> List[Path]:

        self.logger.debug(f"Searching all modules in {workdir} like {module_name}")

        modules_path_list = [path for path in workdir.rglob(module_name)]

        self.logger.debug(f"Found {len(modules_path_list)} modules in {workdir} :: %s", modules_path_list)

        return modules_path_list
