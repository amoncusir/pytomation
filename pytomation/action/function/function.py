import functools
import inspect
from inspect import Signature
from typing import Callable

from pytomation.action.contract import Action, ActionResult
from pytomation.action.function.metadata import get_metadata
from pytomation.action.function.wrapper.action import ActionMetadata
from pytomation.utils.store import TypedStore


class FunctionAction(Action):

    _function: Callable

    def __init__(self, function: Callable):
        super().__init__()
        self._function = function

    @property
    def action_metadata(self) -> ActionMetadata:
        return self.metadata[ActionMetadata]

    @functools.cached_property
    def name(self) -> str:
        return self.action_metadata.name or self._function.__name__

    @functools.cached_property
    def docs(self) -> str:
        return inspect.getdoc(self._function)

    @functools.cached_property
    def signature(self) -> Signature:
        return inspect.signature(self._function)

    @functools.cached_property
    def metadata(self) -> TypedStore:
        return get_metadata(self._function)

    def run(self, *args, **kwargs) -> ActionResult:

        self._logger.debug(f"Running action: {self.name} with parameters: {args}, {kwargs}")

        try:
            result = self._function(*args, **kwargs)
            return ActionResult(True, result, None)
        except BaseException as e:
            return ActionResult(False, None, e)
