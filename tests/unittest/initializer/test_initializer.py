from time import time
from typing import NewType
from unittest.mock import Mock


class SetObjectChain(InitializationChain):

    def __init__(self, order, value):
        super().__init__(order)

        self.value = value

    def handle(self, handler):
        handler.put(self.value)

        handler.next()


def test_init_return_context_objects():
    # Instance the Initializer
    init = Initializer()

    mock = Mock()

    init.add(SetObjectChain(order=0, value=mock))

    # Run the init process
    result = init()

    # Retrieve the value instance
    returned_mock = result.get(type(Mock))

    assert returned_mock is not None
    assert returned_mock == mock


def test_init_share_objects_between_chains():

    class DoubleNumberChain(InitializationChain):

        def handle(self, handler):

            number = handler.get(int)
            handler.put(number * 2, type=int)

            handler.next()

    # Instance the Initializer
    init = Initializer()

    init.add(SetObjectChain(order=0, value=5))
    init.add(DoubleNumberChain(order=10))

    result = init()

    value = result.get(int)

    assert value == 10


def test_init_order_of_chains():

    class TimeChain(InitializationChain):

        time_type: type

        def __init__(self, order, time_type):
            super().__init__(order)
            self.time_type = time_type

        def handle(self, handler):
            handler.put(time(), type=self.time_type)
            handler.next()

    first = NewType("first", float)
    second = NewType("second", float)
    third = NewType("third", float)

    # Instance the Initializer
    init = Initializer()

    init.add(TimeChain(order=0, time_type=first))
    init.add(TimeChain(order=1, time_type=second))
    init.add(TimeChain(order=2, time_type=third))

    result = init()

    first = result.get(first)
    second = result.get(second)
    third = result.get(third)

    assert first << second << third
