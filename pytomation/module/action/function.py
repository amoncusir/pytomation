import functools
import inspect
from inspect import Signature
from typing import Any, Callable, Dict, Type

from pytomation.module.action.contract import Action, ActionResult


class FunctionAction(Action):

    _function: Callable

    def __init__(self, function: Callable):
        super().__init__()
        self._function = function

    @functools.cached_property
    def name(self) -> str:
        return self._function.__name__

    @functools.cached_property
    def docs(self) -> str:
        return inspect.getdoc(self._function)

    @functools.cached_property
    def signature(self) -> Signature:
        return inspect.signature(self._function)

    @functools.cached_property
    def metadata(self) -> Dict[Type, Any]:
        # noinspection PyUnresolvedReferences
        return self._function.__pytomation__

    def get_metadata(self, mtd_type: Type = None) -> Any:
        metadata = self.metadata

        if mtd_type is None:
            return metadata

        return metadata[mtd_type]

    def run(self, *args, **kwargs) -> ActionResult:

        self._logger.debug(f"Running action: {self.name} with parameters: {args}, {kwargs}")

        try:
            result = self._function(*args, **kwargs)
            return ActionResult(True, result, None)
        except BaseException as e:
            return ActionResult(False, None, e)
