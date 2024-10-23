from typing import Any

from pytomation.module import Module
from pytomation.module.loader.source import SourceLoader


# noinspection PyProtectedMember
def import_module(module: Module) -> Any:
    if isinstance(module._loader, SourceLoader):
        if not module.is_loaded:
            module._loader.load()
        return module._loader._python_module
