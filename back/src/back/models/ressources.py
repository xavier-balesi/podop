from typing import ClassVar, Literal

from pydantic import BaseModel, Field


class BaseRessource(BaseModel):
    """Base data model that can be listed in :class:`~back.models.transaction.Transaction`."""

    def __init_subclass__(cls, **kwargs):
        """
        Avoid having the error: "Unable to extract tag using discriminator 'type'"
        at runtime. We directly see the problem at import time.
        """
        # __init_subclass__ avoid having to use a metaclass in this use case
        super().__init_subclass__(**kwargs)
        if cls.__name__ != "IncIdRessource" and "type" not in cls.__dict__:
            raise TypeError(f"The class {cls.__name__} must have a 'type' field.")


class IncIdRessource(BaseRessource):
    _last_id: ClassVar[int] = -1
    id: int
    lock: bool = Field(default=False, exclude=True)

    @classmethod
    def build(cls, *args, **kwargs):
        cls._last_id += 1
        return cls(*args, id=cls._last_id, **kwargs)

    @classmethod
    def reset(cls):
        cls._last_id = -1


class Foo(IncIdRessource):
    type: Literal["foo"] = "foo"


class Bar(IncIdRessource):
    type: Literal["bar"] = "bar"


class FooBar(IncIdRessource):
    type: Literal["foobar"] = "foobar"
    foo_id: int
    bar_id: int


class Money(BaseRessource):
    type: Literal["money"] = "money"
    value: int = 0  # in euros

    def __add__(self, other):
        self.value += other.value
        return self

    def __sub__(self, other):
        self.value -= other.value
        return self
