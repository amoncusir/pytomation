import functools
from functools import WRAPPER_UPDATES

ACTION_ASSIGNED = (
    "__module__",
    "__name__",
    "__qualname__",
    "__doc__",
    "__annotations__",
    "__type_params__",
    "__pytomation__",
)
ACTION_UPDATES = WRAPPER_UPDATES


def wraps_action(fn):
    return functools.wraps(fn, ACTION_ASSIGNED, ACTION_UPDATES)
