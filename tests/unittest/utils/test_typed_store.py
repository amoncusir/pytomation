from typing import List, NewType, TypeVar

import pytest

from pytomation.utils.store import TypedStore


class MyClass:
    id: int

    def __init__(self, _id: int):
        self.id = _id


class MySuperClass(MyClass):
    pass


MyCustomType = NewType("MyCustomType", str)


STORE_VALUES = [
    (int, 1),
    (float, 3.14),
    (str, "hello"),
    (tuple, (1, 2, 3)),
    (List[str], ["one", "two", "three"]),
    (List[int], [1, 2, 3]),
    (MyClass, MyClass(1)),
    (MySuperClass, MySuperClass(2)),
    (MyCustomType, MyCustomType("amzng")),
]


@pytest.mark.parametrize("value_type, value", STORE_VALUES)
def test_set_and_get_individual_value(value_type, value):
    store = TypedStore()

    store[value_type] = value

    assert store[value_type] == value


def test_set_and_get_all_values():
    store = TypedStore()

    for value_type, value in STORE_VALUES:
        store[value_type] = value

    for value_type, value in STORE_VALUES:
        assert store[value_type] == value


@pytest.mark.parametrize("value_type, value", STORE_VALUES)
def test_set_and_delete_individual_value(value_type, value):
    store = TypedStore()

    store[value_type] = value

    del store[value_type]

    assert store.get(value_type) is None


@pytest.mark.parametrize("value_type, value", STORE_VALUES)
def test_set_and_delete_individual_getitem_rise_error(value_type, value):
    store = TypedStore()

    store[value_type] = value

    del store[value_type]

    with pytest.raises(KeyError):
        assert store[value_type] is None


def test_set_and_iterate_values():
    store = TypedStore()

    for value_type, value in STORE_VALUES:
        store[value_type] = value

    assert list(iter(store)) == STORE_VALUES
