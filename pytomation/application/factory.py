from abc import abstractmethod
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from pytomation.configuration import Configuration
    from pytomation.module import Module


class ConfigurationFactory:

    @abstractmethod
    def build(self, configuration: Optional[Configuration]) -> Configuration:
        pass


class ModulesFactory:

    @abstractmethod
    def build(self, configuration: Configuration) -> Dict[str, Module]:
        pass
