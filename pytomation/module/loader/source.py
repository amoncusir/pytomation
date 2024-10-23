import importlib
import importlib.util
import os
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import Any, List, Optional

from pytomation.action import Action
from pytomation.action.function.factory import build_actions_from_python_module
from pytomation.module import Module
from pytomation.module.loader import ModuleLoader
from pytomation.module.metadata import MetadataModule


def builder(source_path: Path, root_path: Path, *_) -> Module:
    mod_name = source_path.name
    mod_dir = source_path.parent.absolute()
    loader = SourceLoader(root_path, mod_dir, mod_name)
    return Module(loader)


class SpecMetadataModule(MetadataModule):
    module_name_prefix: str
    module_spec: ModuleSpec
    module: Optional[Any]

    def __init__(self, module_name_prefix: str, spec: ModuleSpec, module: Optional[Any]):
        self.module_name_prefix = module_name_prefix
        self.module_spec = spec
        self.module = module

    @property
    def qualified_name(self) -> str:
        # Normalize the name for the domain
        return self.module_spec.name.replace(f"{self.module_name_prefix}", "").lstrip(".")

    @property
    def docs(self) -> Optional[str]:
        if self.module is not None and hasattr(self.module, "__doc__"):
            return self.module.__doc__
        return None

    @property
    def module_path(self) -> Optional[Path]:
        if self.module_spec.has_location:
            return Path(self.module_spec.origin).absolute()
        return None

    @property
    def dir_path(self) -> Optional[Path]:
        if self.module_spec.has_location:
            return Path(os.path.dirname(self.module_spec.origin)).absolute()
        return None


class SourceLoader(ModuleLoader):
    root_path: Path
    src_path: Path
    module_name: str
    module_name_prefix: str

    _module_spec: ModuleSpec = None
    _python_module: Any = None

    def __init__(
        self, root_path: Path, src_path: Path, module_name: str, module_name_prefix: str = "pytomation.dynamic.modules"
    ):
        self.root_path = root_path
        self.src_path = src_path
        self.module_name = module_name
        self.module_name_prefix = module_name_prefix
        self._pre_load()

    @property
    def is_loaded(self) -> bool:
        return self._python_module is not None

    @property
    def metadata(self) -> MetadataModule:
        return SpecMetadataModule(self.module_name_prefix, self._module_spec, self._python_module)

    @property
    def actions(self) -> List[Action]:
        return build_actions_from_python_module(self._python_module)

    def _pre_load(self):
        module_name = self._generate_module_name()

        self._module_spec = importlib.util.spec_from_file_location(module_name, self._module_file_path())

    def load(self):
        if self.is_loaded:
            self.reload()  # Reload the module
            return

        # Generate the module
        unload_module = importlib.util.module_from_spec(self._module_spec)
        self._module_spec.loader.exec_module(unload_module)  # Load the module
        self._python_module = unload_module

    def reload(self):
        if not self.is_loaded:
            raise ValueError("Cannot reload module. First load the module")

        importlib.reload(self._python_module)

    def _generate_module_name(self) -> str:
        qualified_path = (
            str(self.src_path.absolute()).replace(str(self.root_path.absolute()), "").strip("/").replace("/", ".")
        )

        if qualified_path == "":  # Root module
            return self.module_name_prefix

        return f"{self.module_name_prefix}.{qualified_path}"

    def _module_file_path(self) -> Path:
        module_path = self.src_path.absolute() / self.module_name

        if module_path.is_file():
            return module_path

        raise ValueError(f"Cannot find module file at {module_path}")
