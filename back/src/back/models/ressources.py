from typing import ClassVar, Literal

from pydantic import BaseModel, Field


class IncIdRessource(BaseModel):
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
