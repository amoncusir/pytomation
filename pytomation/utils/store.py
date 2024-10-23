from typing import Dict, Type, TypeVar

ValueType = TypeVar("ValueType")


class TypedStore:

    _store: Dict[Type[ValueType], ValueType]

    def __init__(self, store: Dict[Type[ValueType], ValueType] = None):
        if store is None:
            store = {}

        self._store = store

    def put(self, value: ValueType, *, type_value: Type[ValueType] | Type = None):
        if type_value is None:
            type_value = type(value)

        self._store[type_value] = value

    def get(self, type_value: Type[ValueType], default=None) -> ValueType:
        return self._store.get(type_value, default)

    def delete(self, type_value: Type[ValueType]):
        del self._store[type_value]

    def __getitem__(self, item: Type[ValueType]) -> ValueType:
        return self._store[item]

    def __setitem__(self, key: Type[ValueType], value: ValueType):
        self.put(value, type_value=key)

    def __delitem__(self, key: Type[ValueType]):
        self.delete(key)

    def __contains__(self, item: Type[ValueType]):
        return item in self._store

    def __iter__(self):
        return iter(self._store.items())

    def __repr__(self):
        return f"TypedStore({repr(self._store)})"
