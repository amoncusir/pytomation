import functools

from pytomation.action_wrapper.util import safe_call, get_context
from .executor import depends_on_executor


def run_before(qualified_action_path: str):

    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            depends_on_executor(qualified_action_path, get_context(kwargs))
            return safe_call(fn, *args, **kwargs)

        return inner

    return wrapper


def run_after(qualified_action_path: str):

    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            result = safe_call(fn, *args, **kwargs)
            depends_on_executor(qualified_action_path, get_context(kwargs))
            return result

        return inner

    return wrapper
