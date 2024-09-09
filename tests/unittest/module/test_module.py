from pathlib import Path
from unittest.mock import Mock

import pytest

from pytomation.errors import ImmutableChangeError
from pytomation.module import Module


def build_action(name: str):
    action_mock = Mock()
    action_mock.configure_mock(name=name)
    return action_mock


def build_module(
    name="module", docs="My Module docs!", path=Path("/test/module"), actions=None, children=tuple(), freeze=True
) -> Module:

    if actions is None:
        actions = [
            build_action("print_action"),
            build_action("useful_action"),
        ]

    module = Module(name=name, docs=docs, path=path, actions=actions, children=children)

    if freeze:
        module.freeze()

    return module


def test_module_name():

    module = build_module(name="test_module")

    assert module.name == "test_module"


def test_module_docs():

    module = build_module()

    assert module.docs == "My Module docs!"


def test_module_path():

    module = build_module()

    assert module.path == Path("/test/module")


def test_module_actions():

    module = build_module()

    actions = module.actions

    assert len(actions) == 2


def test_module_actions_magic_method_getitem():
    module = build_module()

    action = module["print_action"]

    assert action is not None
    assert action.name == "print_action"


def test_module_actions_magic_method_contains():
    module = build_module()

    assert "print_action" in module


def test_module_root():
    child_two_module = build_module(name="two", freeze=False)
    child_one_module = build_module(name="one", children=(child_two_module,), freeze=False)
    root_module = build_module(name="root", children=(child_one_module,))

    assert root_module.root == root_module
    assert child_one_module.root == root_module
    assert child_two_module.root == root_module


def test_module_parent():
    child_two_module = build_module(name="two", freeze=False)
    child_one_module = build_module(name="one", children=(child_two_module,), freeze=False)
    root_module = build_module(name="root", children=(child_one_module,))

    assert root_module.parent is None
    assert child_one_module.parent == root_module
    assert child_two_module.parent == child_one_module


def test_module_parent_immutability():
    child_two_module = build_module(name="two", freeze=False)
    child_one_module = build_module(name="one", children=(child_two_module,), freeze=False)
    root_module = build_module(name="root", children=(child_one_module,))

    with pytest.raises(ImmutableChangeError):
        root_module._add_child(child_two_module)


def test_module_children():
    child_two_one_module = build_module(name="two_one", freeze=False)
    child_one_two_module = build_module(name="one_two", freeze=False)
    child_one_one_module = build_module(name="one_one", children=(child_two_one_module,), freeze=False)
    root_module = build_module(name="root", children=(child_one_one_module, child_one_two_module))

    assert root_module.children == (child_one_one_module, child_one_two_module)
    assert child_one_one_module.children == (child_two_one_module,)
    assert child_two_one_module.children == tuple()
