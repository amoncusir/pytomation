import inspect
from collections.abc import Callable
from typing import Any, List

from pytomation.action import Action
from pytomation.action.function.function import FunctionAction
from pytomation.action.function.wrapper.action import is_action


def build_action(func: Callable) -> Action:
    return FunctionAction(func)


def build_actions_from_python_module(py_mod: Any) -> List[Action]:
    return [build_action(fn[1]) for fn in inspect.getmembers(py_mod, is_action)]
