import logging
from abc import abstractmethod
from dataclasses import dataclass
from inspect import Signature
from typing import Any, Optional, Type

from pytomation.utils.store import TypedStore


@dataclass(frozen=True)
class ActionResult:

    success: bool
    result: Optional[Any]
    error: Optional[BaseException]


class Action:

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__qualname__)

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def docs(self) -> str: ...

    @property
    @abstractmethod
    def signature(self) -> Signature: ...

    @abstractmethod
    def run(self, *args, **kwargs) -> ActionResult: ...

    @abstractmethod
    def metadata(self) -> TypedStore: ...
