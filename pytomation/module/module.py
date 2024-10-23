import functools
from pathlib import Path
from typing import Dict, List, Optional, Self

from pytomation.action import Action
from pytomation.module.loader import ModuleLoader
from pytomation.module.metadata import MetadataModule
from pytomation.utils.graph import ReverseTree


class Module(ReverseTree[Self]):
    """
    Facade class that contains all the logic
    """

    _loader: ModuleLoader
    _actions: Dict[str, Action]
    _metadata: MetadataModule

    def __init__(self, loader: ModuleLoader):
        if loader is None:
            raise ValueError("Loader cannot be None")

        super().__init__()

        self._loader = loader
        self._metadata = self._loader.metadata

    @property
    def qualified_name(self) -> str:
        return self._metadata.qualified_name

    @property
    def docs(self) -> Optional[str]:
        if not self.is_loaded:
            self.load()

        return self._metadata.docs

    @property
    def module_path(self) -> Optional[Path]:
        return self._metadata.module_path

    @property
    def dir_path(self) -> Optional[Path]:
        return self._metadata.dir_path

    @property
    def is_loaded(self) -> bool:
        return self._loader.is_loaded

    @functools.cached_property
    def actions(self) -> List[Action]:
        if not self.is_loaded:
            self.load()

        return list(self._actions.values())

    def __getitem__(self, item):
        if not self.is_loaded:
            self.load()

        return self._actions[item]

    def __contains__(self, item):
        if not self.is_loaded:
            self.load()

        return item in self._actions.keys()

    def load(self):
        if self.parent is not None:
            self.parent.load()

        self._load()

    def _load(self):
        if not self.is_loaded:
            self._loader.load()
        else:
            self._loader.reload()

        self._metadata = self._loader.metadata
        self._actions = {a.name: a for a in self._loader.actions}
