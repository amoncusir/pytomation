import functools
import logging

from pytomation.action_wrapper.util import safe_call


def action():
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return safe_call(fn, *args, **kwargs)

        inner.__action__ = True
        logging.debug(
            f"Registered action: {inner.__name__} on {inner.__code__.co_filename}:{inner.__code__.co_firstlineno}"
        )
        return inner

    return wrapper
