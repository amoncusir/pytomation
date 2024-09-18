from abc import abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pytomation.configuration import Configuration
    from pytomation.module import Module


class ModulesFactory:

    @abstractmethod
    def build(self, configuration: Configuration) -> Dict[str, Module]:
        pass
