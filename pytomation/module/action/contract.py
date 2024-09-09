import logging
from abc import abstractmethod
from dataclasses import dataclass
from inspect import Signature
from typing import Any, Optional, Type


@dataclass(frozen=True)
class ActionResult:

    success: bool
    result: Optional[Any]
    error: Optional[BaseException]


class Action:

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def docs(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def signature(self) -> Signature:
        raise NotImplementedError

    @abstractmethod
    def run(self, *args, **kwargs) -> ActionResult:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, mtd_type: Type) -> Any:
        raise NotImplementedError
