from typing import Type


class InitializerError(Exception):
    pass


class ObjectNotFoundOnInitialization(InitializerError):
    type: Type

    def __init__(self, type_: Type) -> None:
        self.type = type_
        super().__init__(f"Object {type_} not found in initialization context")
