import inspect
import logging
from abc import abstractmethod
from operator import attrgetter
from typing import TYPE_CHECKING, List, Sequence

from pytomation.action_wrapper.util import safe_call

if TYPE_CHECKING:
    from pytomation.context import Context


class Action:

    name: str
    parameters: List[str]
    docs: str

    def __init__(self, name: str, parameters: List[str], docs: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.parameters = parameters
        self.docs = docs

        self._logger.debug(f"Action <{name}> initialized")

    def __repr__(self):
        return f"<Action {self.name}: {self.docs}>"

    @abstractmethod
    def run(self, context: "Context"):
        pass


class FunctionAction(Action):

    def __init__(self, fn: any):
        signature = inspect.signature(fn)
        docs = inspect.getdoc(fn)
        parameters = list(map(attrgetter("name"), signature.parameters.values()))

        super().__init__(fn.__name__, parameters, docs)
        self.fn = fn
        self.fn_parameters = signature.parameters

    def run(self, context: "Context"):
        self._logger.debug(f"Running action: {self.name}")
        self._logger.debug("\tWith context: %s", context)

        safe_call(self.fn, context=context, **context.__dict__)


def _extract_dependencies(fn) -> Sequence[str]:
    if hasattr(fn, "__depends_on__"):
        return fn.__depends_on__
    return tuple()
