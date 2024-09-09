from unittest.mock import Mock

import pytest

from pytomation.context.context_caller import ContextCaller


def build_caller() -> ContextCaller:
    return ContextCaller(
        module=Mock(),
        action=Mock(),
        arguments=(
            "-v",
            "3",
            "--no-value",
            "--with-value",
            "hello world",
            "--multiple-values",
            "one",
            "2",
            "three",
            "-s",
        ),
    )


def test_context_caller_module():
    caller = build_caller()

    module = caller.module

    assert module is not None


def test_context_caller_action():
    caller = build_caller()

    action = caller.action

    assert action is not None


def test_context_caller_parameters():
    caller = build_caller()

    arguments = caller.arguments

    assert arguments == (
        "-v",
        "3",
        "--no-value",
        "--with-value",
        "hello world",
        "--multiple-values",
        "one",
        "2",
        "three",
        "-s",
    )


@pytest.mark.parametrize("arg", ["--no-value", "-v", ("-s", "--short"), ("-w", "--with-value"), ("--multiple-values",)])
def test_context_caller_contains(arg):
    caller = build_caller()

    assert arg in caller


@pytest.mark.parametrize(
    "arg, value",
    [
        (("--no-value", "-n"), tuple()),
        ("--no-value", tuple()),
        pytest.param("-n", None, marks=pytest.mark.xfail),
        (("--short", "-s"), tuple()),
        pytest.param("--short", None, marks=pytest.mark.xfail),
        ("-s", tuple()),
        (("--with-value", "-w"), ("hello world",)),
        (("--value", "-v"), ("3",)),
        (("--multiple-values", "-m"), ("one", "2", "three")),
    ],
)
def test_context_caller_getitem(arg, value):
    caller = build_caller()

    assert caller[arg] == value
