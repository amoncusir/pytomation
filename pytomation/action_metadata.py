import functools

from pytomation.action_wrapper.util import safe_call


def action():
    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return safe_call(fn, *args, **kwargs)

        inner.__action__ = True
        return inner

    return wrapper
