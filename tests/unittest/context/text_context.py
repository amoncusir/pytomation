from typing import Callable, Tuple

from pytomation.context import Context


def build_context() -> Context:
    pass


def test_context_caller():
    context = build_context()

    caller = context.caller

    assert caller.module is not None
    assert caller.module.name == ""

    assert caller.action is not None
    assert caller.action.name == "print"

    assert caller.arguments is Tuple[str, ...]


def test_context_action_log():
    context = build_context()

    handler = context.action_handler

    assert handler.step is int
    assert handler.step <= 0

    assert handler.size is int
    assert handler.size <= 0

    assert handler.roadmap is tuple
    assert handler.roadmap[handler.step].action is not None
    assert handler.roadmap[handler.step].module is not None

    assert handler.current is not None

    assert handler.stop_handling is Callable[[None], None]


def test_context_store():
    context = build_context()

    store = context.store

    assert store is not None
    assert store is TypedStore
