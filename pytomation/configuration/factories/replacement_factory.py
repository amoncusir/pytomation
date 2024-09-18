from pathlib import Path
from typing import Any, Iterable, Tuple, Type, TypeVar

from pytomation.configuration import Configuration
from pytomation.configuration.factory import ConfigurationFactory

IgnoreType = TypeVar("IgnoreType")


class ConfigurationReplacement:

    module_name: str | Type[IgnoreType]
    module_path_splitter: str | Type[IgnoreType]
    call_path: Path | Type[IgnoreType]
    project_path: Path | Type[IgnoreType]
    verbosity: int | Type[IgnoreType]

    def __init__(self):
        self.module_name = IgnoreType
        self.module_path_splitter = IgnoreType
        self.call_path = IgnoreType
        self.project_path = IgnoreType
        self.verbosity = IgnoreType

    def __iter__(self):
        return iter(self.__dict__.values())


class ReplacementFactory(ConfigurationFactory):

    replacement: ConfigurationReplacement | Iterable[Tuple[str, Any]]

    def __init__(self, replacement: ConfigurationReplacement | Iterable[Tuple[str, Any]]):
        self.replacement = replacement

    def build(self, configuration: Configuration) -> Configuration:
        return self.replace_configuration(configuration)

    def replace_configuration(self, configuration: Configuration) -> Configuration:

        replacements = iter(self.replacement)
        trans_dict = {}

        for attr, value in replacements:
            if value is not IgnoreType:
                trans_dict[attr] = value

        return configuration.copy(**trans_dict)
