import functools
import importlib.util
import inspect
import logging
import os.path
import shutil
from abc import abstractmethod
from os import PathLike
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Self

from pytomation.action import TYPE_CHECKING, Action, FunctionAction
from pytomation.errors import RunnerActionNotFoundError
from pytomation.file_builder.local_file_builder import LocalFileBuilder
from pytomation.utils import command

if TYPE_CHECKING:
    from pytomation.context import Context
    from pytomation.file_builder.file_builder import FileBuilder


def is_fn_action(fn):
    return inspect.isfunction(fn) and hasattr(fn, "__action__")


class Module:

    is_executed: bool
    actions: Dict[str, Action]
    children: List[Self]
    parent: Optional[Self]

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.is_executed = False
        self.parent = None
        self.children = []
        self.actions = {}

    def __repr__(self):
        return f"<lc module;{self.is_executed};{self.name}{self.actions}>"

    def __contains__(self, item):
        return item in self.actions.keys()

    @functools.cached_property
    def root_module(self) -> Self:

        def get_root(module: Self) -> Self:
            if module.parent is None:
                return module

            return get_root(module.parent)

        return get_root(self)

    @functools.cached_property
    def deep_children(self) -> Dict[str, Self]:

        def append_children(node: Module, children: Dict[str, Module]):
            for child in node.children:
                children[child.name] = child
                append_children(child, children)

        children_root = {}
        append_children(self, children_root)

        return children_root

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def docs(self) -> str:
        pass

    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def run_action(self, name: str, context: "Context") -> bool:
        pass

    def get_file_builder(self) -> "FileBuilder":
        return LocalFileBuilder(self.path)

    def run_command(self, *cmd: any, timeout=None, check=True, env=None):
        self._logger.debug(f"Running command: %s, {timeout}, {check}, %s", cmd, env)
        return command.run(self.path, *cmd, timeout=timeout, check=check, env=env)

    def copy_file(self, src: Path, dst: Path, abs_path=False):

        src = self.path / src
        dst = dst if abs_path else self.path / dst

        self._logger.debug(f"Copying {src} to {dst}")

        shutil.copyfile(str(src), str(dst))

    def append_child(self, child):
        self.children.append(child)

    def sorted_children(self) -> Iterable[Self]:
        return sorted(self.children, key=lambda m: m.name)

    def build_path(self, name) -> Path:
        return self.path.joinpath(name)


class SourceFileModule(Module):

    @staticmethod
    def load_from_file(name: str, path: PathLike):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        return SourceFileModule(spec, module)

    def __init__(self, module_spec, module):
        super().__init__()
        self.module_spec = module_spec
        self.module = module

        self._logger.debug(f"Module <{self.name}> initialized")

    @property
    def name(self) -> str:
        return self.module_spec.name

    @property
    def docs(self) -> str:
        if not self.is_executed:
            self.load()

        return self.module.__doc__

    @property
    def path(self) -> Path:
        if self.module_spec.has_location:
            return Path(os.path.dirname(self.module_spec.origin))
        raise RuntimeError("Module has not path")

    def load(self):
        self._logger.debug(f"Loading {self.name}")

        if self.is_executed:
            self._logger.error("Module already executed")
            raise RuntimeError("Module already executed")

        self.module_spec.loader.exec_module(self.module)
        self.is_executed = True

        self.actions = {fn[0]: FunctionAction(fn[1]) for fn in inspect.getmembers(self.module, is_fn_action)}
        self._logger.debug(f"Loaded {self.name} with actions: {self.actions}")

    def run_action(self, name: str, context: "Context", base_module: Self = None, optional: bool = False) -> bool:
        self._logger.debug(f"Running action {name} with context: %s extended by {base_module}", context)

        if not self.is_executed:
            self.load()

        if name not in self.actions:
            if not optional:
                self._logger.warning(f"Action {name} not found")
                raise RunnerActionNotFoundError(name, self)

            return False

        action = self.actions[name]

        if base_module is None:
            action.run(context)
        else:
            action.run(context.extend_from_module(self))

        for child in self.sorted_children():
            child.run_action(name, context, base_module if base_module is not None else self, True)

        return True
