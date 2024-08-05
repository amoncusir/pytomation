import functools
from typing import TYPE_CHECKING, List

from pytomation.action_wrapper.util import get_from_context, safe_call

if TYPE_CHECKING:
    from pytomation.profile import Profile


def profile(with_profiles: List[str] = None, without_profiles: List[str] = None):

    if with_profiles is None and without_profiles is None:
        raise ValueError("One of with_profiles or without_profiles must be specified")
    if with_profiles is not None and without_profiles is not None:
        raise ValueError("Only one of with_profiles or without_profiles must be specified")

    #  100% this can be optimized!
    if with_profiles is not None:

        def execute(cprofile: "Profile") -> bool:
            for p in with_profiles:
                if p in cprofile.profiles:
                    return True
            return False

    else:

        def execute(cprofile: "Profile") -> bool:
            for p in without_profiles:
                if p in cprofile.profiles:
                    return False
            return True

    def wrapper(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            cprofile = get_from_context(kwargs, "profile")

            if execute(cprofile):
                return safe_call(fn, *args, **kwargs)

        return inner

    return wrapper
