from abc import abstractmethod
from pathlib import Path
from typing import Optional, Protocol


class MetadataModule(Protocol):

    @property
    @abstractmethod
    def qualified_name(self) -> str: ...

    @property
    @abstractmethod
    def docs(self) -> Optional[str]: ...

    @property
    @abstractmethod
    def module_path(self) -> Optional[Path]: ...

    @property
    @abstractmethod
    def dir_path(self) -> Optional[Path]: ...
