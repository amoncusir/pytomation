from typing import NewType
from unittest.mock import Mock

from pytomation.initializer.context import ContextHandler


class MyClass:
    id: int

    def __init__(self, _id: int):
        self.id = _id


class MySuperClass(MyClass):
    pass


MyCustomType = NewType("MyCustomType", str)


def test_context_handler_get():

    negative = NewType("negative", int)

    ctx = ContextHandler(
        {
            int: 1,
            negative: -1,
            float: 3.14,
            str: "Hello",
            Mock: Mock(id="mock"),
            MyClass: MyClass(1),
            MySuperClass: MySuperClass(2),
            MyCustomType: MyCustomType("amzng"),
        }
    )

    assert ctx.get(int) == 1
    assert ctx.get(negative) == -1
    assert ctx.get(float) == 3.14
    assert ctx.get(str) == "Hello"
    assert ctx.get(Mock).id == "mock"
    assert isinstance(ctx.get(MyClass), MyClass)
    assert ctx.get(MyClass).id == 1
    assert isinstance(ctx.get(MySuperClass), MySuperClass)
    assert ctx.get(MySuperClass).id == 2
    assert ctx.get(MyCustomType) == "amzng"


def test_context_handler_put():
    negative = NewType("negative", int)

    ctx = ContextHandler()

    ctx.put(1)
    ctx.put(-1, negative)
    ctx.put(3.14)
    ctx.put("Hello")
    ctx.put(Mock(id="mock"), Mock)
    ctx.put(MyClass(1))
    ctx.put(MySuperClass(2))
    ctx.put(MyCustomType("amzng"), MyCustomType)

    store = ctx.store

    assert store.get(int) == 1
    assert store.get(negative) == -1
    assert store.get(float) == 3.14
    assert store.get(str) == "Hello"
    assert ctx.get(Mock).id == "mock"
    assert isinstance(store.get(MyClass), MyClass)
    assert store.get(MyClass).id == 1
    assert isinstance(store.get(MySuperClass), MySuperClass)
    assert store.get(MySuperClass).id == 2
    assert store.get(MyCustomType) == "amzng"


def test_context_handler_put_and_get():

    negative = NewType("negative", int)

    ctx = ContextHandler()

    ctx.put(1)
    ctx.put(-1, negative)
    ctx.put(3.14)
    ctx.put("Hello")
    ctx.put(Mock(id="mock"), Mock)
    ctx.put(MyClass(1))
    ctx.put(MySuperClass(2))
    ctx.put(MyCustomType("amzng"), MyCustomType)

    assert ctx.get(int) == 1
    assert ctx.get(negative) == -1
    assert ctx.get(float) == 3.14
    assert ctx.get(str) == "Hello"
    assert ctx.get(Mock).id == "mock"
    assert isinstance(ctx.get(MyClass), MyClass)
    assert ctx.get(MyClass).id == 1
    assert isinstance(ctx.get(MySuperClass), MySuperClass)
    assert ctx.get(MySuperClass).id == 2
    assert ctx.get(MyCustomType) == "amzng"
