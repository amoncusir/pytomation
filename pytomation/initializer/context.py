from typing import Any, Dict, Type, TypeVar

ValueType = TypeVar("ValueType")


class ContextHandler:

    store: Dict[ValueType, Any]

    def __init__(self, store: Dict[ValueType, Any] = None):
        if store is None:
            store = {}

        self.store = store

    def put(self, value: ValueType, type_value: Type[ValueType] | Type = None):
        if type_value is None:
            type_value = type(value)

        self.store[type_value] = value

    def get(self, type_value: Type[ValueType]) -> ValueType:
        return self.store.get(type_value)
