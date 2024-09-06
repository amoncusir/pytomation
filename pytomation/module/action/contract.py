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


#
# class FunctionAction(Action):
#
#     def __init__(self, fn: any):
#         signature = inspect.signature(fn)
#         docs = inspect.getdoc(fn)
#         parameters = list(map(attrgetter("name"), signature.parameters.values()))
#
#         super().__init__(fn.__name__, parameters, docs)
#         self.fn = fn
#         self.fn_parameters = signature.parameters
#
#     def run(self, context: "Context"):
#         self._logger.debug(f"Running action: {self.name}")
#         self._logger.debug("\tWith context: %s", context)
#
#         safe_call(self.fn, context=context, **context.__dict__)
#
#
# def _extract_dependencies(fn) -> Sequence[str]:
#     if hasattr(fn, "__depends_on__"):
#         return fn.__depends_on__
#     return tuple()
