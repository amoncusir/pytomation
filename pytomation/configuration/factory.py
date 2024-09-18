from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytomation.configuration import Configuration


class ConfigurationFactory:

    @abstractmethod
    def build(self, configuration: "Configuration") -> "Configuration":
        pass
