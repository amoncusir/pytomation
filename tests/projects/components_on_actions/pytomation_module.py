from typing import TypeVar

UniqueType = TypeVar("UniqueType", bound=str)


@component()
def optional_name_if_its_unique() -> UniqueType:
    return "unique!"


MultipleType = TypeVar("MultipleType", bound=str)


@component()
def multiple_one(unq: UniqueType) -> MultipleType:
    assert unq == "unique!"

    return "one!"


@component(name="multiple_two")
def multiple_two_builder() -> MultipleType:
    return "two!"


@action()
def no_dependency():
    pass


@action()
def with_dependency(unique: UniqueType, multiple_one: MultipleType, multiple_two: MultipleType):
    assert unique == "unique!"
    assert multiple_one == "one!"
    assert multiple_two == "two!"
