from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Protocol, Sequence

from pytomation.initializer.errors import ObjectNotFoundOnInitialization
from pytomation.initializer.initializer import InitializationChain
from pytomation.initializer.types import ModulesPath, ModuleTree, RootPath
from pytomation.module import Module
from pytomation.utils.store import TypedStore


class ModuleBuilder(Protocol):

    def __call__(self, source_path: Path, root_path: Path, context: TypedStore) -> Module: ...


class ModuleBuilderChain(InitializationChain):

    builder: ModuleBuilder

    def __init__(self, builder: ModuleBuilder, order: int = 0):
        super().__init__(order)
        self.builder = builder

    def process(self, next_handler: Callable[[TypedStore], TypedStore], context: TypedStore) -> TypedStore:
        if ModulesPath not in context:
            raise ObjectNotFoundOnInitialization(ModulesPath)

        if RootPath not in context:
            raise ObjectNotFoundOnInitialization(RootPath)

        modules = self.build_modules(context)

        context.put(modules, type_value=ModuleTree)

        return next_handler(context)

    def build_modules(self, context: TypedStore) -> Dict[str, Module]:
        modules_path = context[ModulesPath]
        root_path = context[RootPath]
        modules_dict: Dict[str, Module] = {}

        for path in modules_path:
            module = self.builder(path, root_path, context)
            modules_dict[module.qualified_name] = module

        build_tree(modules_dict)

        return modules_dict


def build_tree(modules: Dict[str, Module]):
    no_root = modules.copy()

    if "" in no_root:
        del no_root[""]

    for mod in no_root.values():
        split_name = mod.qualified_name.split(".")
        parent = find_near_parent(modules, split_name)

        if parent is not None:
            parent.add_child(mod)


def find_near_parent(dict_modules: Dict[str, Module], path: Sequence[str]) -> Optional[Module]:
    len_path = len(path)

    for node in reversed(range(len_path)):
        dot_path = ".".join(path[:node])

        if dot_path in dict_modules:
            return dict_modules[dot_path]

    return None
