import inspect
import logging
from dataclasses import dataclass
from inspect import isfunction
from typing import Callable, Optional

from pytomation.action.function.metadata import get_metadata, get_to_put_metadata
from pytomation.action.function.wrapper.utils import wraps_action
from pytomation.utils.store import TypedStore

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ActionMetadata:
    name: Optional[str] = None


def action(name: str = None):
    action_metadata = ActionMetadata(name)

    def wrapper(func):

        @wraps_action(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        metadata = get_to_put_metadata(inner)
        metadata.put(action_metadata)

        if _logger.isEnabledFor(logging.DEBUG):
            root_fn = func.__wrapped__ if hasattr(func, "__wrapped__") else func
            _logger.debug("Register action on %s:%s with %s", inspect.getfile(root_fn), root_fn.__qualname__, metadata)

        return inner

    return wrapper


def is_action(fn: Callable) -> bool:
    if not isfunction(fn):
        return False

    metadata = get_metadata(fn)

    return metadata is not None and isinstance(metadata, TypedStore) and ActionMetadata in metadata
