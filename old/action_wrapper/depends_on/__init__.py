import functools

from old.action_wrapper.util import get_context, safe_call

from .executor import depends_on_executor

# TODO: It works, but no in a right way! Consider new approaches to call actions using some stack or funcy structure...
# What a shame!


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
