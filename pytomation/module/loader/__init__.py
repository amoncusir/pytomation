from abc import abstractmethod
from typing import List

from pytomation.action import Action
from pytomation.module.metadata import MetadataModule


class ModuleLoader:

    @property
    @abstractmethod
    def is_loaded(self) -> bool: ...

    @property
    @abstractmethod
    def metadata(self) -> MetadataModule: ...

    @property
    @abstractmethod
    def actions(self) -> List[Action]: ...

    @abstractmethod
    def load(self):
        """
        Load every time the module and create the context objects to be returned
        """
        ...

    @abstractmethod
    def reload(self):
        """
        Reload from the module source file, the existent code. Must be loaded before runs the method.
        """
        ...
