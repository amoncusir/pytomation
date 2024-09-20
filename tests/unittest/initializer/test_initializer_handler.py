from time import time
from typing import NewType, Type

import pytest

from pytomation.initializer.initializer import InitializationChain, InitializerHandler
from pytomation.utils.store import TypedStore


class SetObjectChain(InitializationChain):

    def __init__(self, order, value):
        super().__init__(order)

        self.value = value

    def process(self, next_handler, context: TypedStore):
        context.put(self.value)

        next_handler(context)


def test_initializer_return_context_objects():
    # Instance the Initializer
    init = InitializerHandler()

    init.add(SetObjectChain(order=0, value=10))

    # Run the init process
    result = init()

    # Retrieve the value instance
    int_ten = result.get(int)

    assert int_ten is not None
    assert int_ten == 10


def test_initializer_share_objects_between_chains():

    class DoubleNumberChain(InitializationChain):

        def process(self, next_handler, context: TypedStore):

            number = context.get(int)
            context.put(number * 2, type_value=int)

            next_handler(context)

    # Instance the Initializer
    init = InitializerHandler()

    init.add(SetObjectChain(order=0, value=5))
    init.add(DoubleNumberChain(order=10))

    result = init()

    value = result.get(int)

    assert value == 10


def test_initializer_order_of_chains():

    class TimeChain(InitializationChain):

        time_type: Type

        def __init__(self, order, time_type):
            super().__init__(order)
            self.time_type = time_type

        def process(self, next_handler, context: TypedStore):
            context.put(time(), type_value=self.time_type)
            next_handler(context)

    first = NewType("first", float)
    second = NewType("second", float)
    third = NewType("third", float)

    # Instance the Initializer
    init = InitializerHandler()

    init.add(TimeChain(order=0, time_type=first))
    init.add(TimeChain(order=1, time_type=second))
    init.add(TimeChain(order=2, time_type=third))

    result = init()

    first = result.get(first)
    second = result.get(second)
    third = result.get(third)

    assert first < second < third


def test_initializer_change_context():

    class FreshContextChain(InitializationChain):

        def process(self, next_handler, context: TypedStore):
            next_handler(TypedStore())

    init = InitializerHandler()

    init.add(SetObjectChain(order=0, value=5))
    init.add(FreshContextChain(order=10))

    result = init()

    assert result._store == {}


def test_initializer_raise_error():

    class RaiseErrorChain(InitializationChain):

        def process(self, next_handler, context: TypedStore):
            raise Exception("Chain Exception")

    init = InitializerHandler()

    init.add(RaiseErrorChain())

    with pytest.raises(Exception) as exc_info:

        init()

        assert "Chain Exception" in str(exc_info.value)


def test_initializer_stop_chain():

    class StopChain(InitializationChain):

        def process(self, next_handler, context: TypedStore):
            pass

    init = InitializerHandler()

    init.add(SetObjectChain(order=0, value=5))
    init.add(StopChain(order=5))
    init.add(SetObjectChain(order=10, value=10))

    result = init()

    int_value = result.get(int)

    assert int_value is not None
    assert int_value == 5
