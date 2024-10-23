from typing import Callable, Final, Optional

from pytomation.utils.store import TypedStore

__METADATA_KEY: Final[str] = "__pytomation__"


def has_metadata(action_fn: Callable) -> bool:
    return hasattr(action_fn, __METADATA_KEY)


def put_metadata(action_fn: Callable, metadata: TypedStore):
    setattr(action_fn, __METADATA_KEY, metadata)


def get_metadata(action_fn: Callable) -> Optional[TypedStore]:
    return getattr(action_fn, __METADATA_KEY, None)


def get_to_put_metadata(action_fn: Callable) -> TypedStore:
    if not has_metadata(action_fn):
        put_metadata(action_fn, TypedStore())

    return get_metadata(action_fn)
