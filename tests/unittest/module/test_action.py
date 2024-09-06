from inspect import Parameter, Signature
from typing import Callable

from pytomation.module.action import Action
from pytomation.module.action.function import FunctionAction


def build_action_from_function(fn: Callable) -> Action:
    return FunctionAction(fn)


def test_action_name():
    def my_action():
        pass

    action = build_action_from_function(my_action)

    assert action.name == "my_action"


def test_action_docs():
    def my_action():
        """my_action docs"""

    action = build_action_from_function(my_action)

    assert action.docs == "my_action docs"


def test_action_no_parameters():
    def my_action():
        pass

    action = build_action_from_function(my_action)

    signature: Signature = action.signature

    assert len(signature.parameters) == 0


def test_action_signature():
    class MyClass:
        pass

    def my_action(number: int, string: str, my_class: MyClass, no_type):
        pass

    signature: Signature = build_action_from_function(my_action).signature

    number_parameter = signature.parameters["number"]
    string_parameter = signature.parameters["string"]
    my_class_parameter = signature.parameters["my_class"]
    no_type_parameter = signature.parameters["no_type"]

    assert len(signature.parameters) == 4

    assert number_parameter.name == "number"
    assert number_parameter.annotation == int

    assert string_parameter.name == "string"
    assert string_parameter.annotation == str

    assert my_class_parameter.name == "my_class"
    assert my_class_parameter.annotation == MyClass

    assert no_type_parameter.name == "no_type"
    assert no_type_parameter.annotation == Parameter.empty


def test_action_get_metadata():
    def my_action():
        pass

    my_action.__pytomation__ = {int: 3}

    action = build_action_from_function(my_action)

    assert action.get_metadata(int) == 3


def test_action_list_metadata():
    def my_action():
        pass

    my_action.__pytomation__ = {int: 3, str: "lol"}

    action = build_action_from_function(my_action)

    assert action.get_metadata() == {int: 3, str: "lol"}


def test_action_run_no_parameters():
    called_flag = False

    def my_action():
        nonlocal called_flag
        called_flag = True

    action = build_action_from_function(my_action)

    action.run()

    assert called_flag


def test_action_run_with_parameters_no_kwargs():
    called_flag = 0

    def my_action(number: int):
        nonlocal called_flag
        called_flag = number

    action = build_action_from_function(my_action)

    action.run(10)

    assert called_flag == 10


def test_action_run_with_parameters_multiple_times():
    called_flag = []

    def my_action(number: int):
        nonlocal called_flag
        called_flag.append(number)

    action = build_action_from_function(my_action)

    action.run(0)
    action.run(10)
    action.run(20)

    assert called_flag == [0, 10, 20]


def test_action_run_with_parameters_kwargs():
    called_flag = 0

    def my_action(number: int):
        nonlocal called_flag
        called_flag = number

    action = build_action_from_function(my_action)

    action.run(number=10)

    assert called_flag == 10


def test_action_run_return():

    def my_action():
        return 3.1415

    action = build_action_from_function(my_action)

    result = action.run()

    assert result.success is True
    assert result.result == 3.1415
    assert result.error is None


def test_action_run_raise_error():

    class MyError(Exception):

        def __init__(self, msg: str):
            self.msg = msg

    def my_action():
        raise MyError("my_action error")

    action = build_action_from_function(my_action)

    result = action.run()

    assert result.success is False
    assert result.result is None
    assert isinstance(result.error, MyError)
    assert result.error.msg == "my_action error"
