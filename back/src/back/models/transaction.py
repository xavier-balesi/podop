from typing import Annotated, ClassVar, Literal

from pydantic import BaseModel, Field

from back import scheduler

# Model = TypeVar("Model", bound=BaseModel)


# class EventType(StrEnum):
#     MINED = auto()
#
# Event = Annotated[
#     EnrichProcessor | RemoveProcessor | SetProcessor | ScriptProcessor,
#     Field(..., discriminator="type"),
# ]


class IncIdRessource(BaseModel):
    _last_id: ClassVar[int] = -1
    id: int

    @classmethod
    def build(cls):
        cls._last_id += 1
        return cls(id=cls._last_id)

    @classmethod
    def reset(cls):
        cls._last_id = -1


class Foo(IncIdRessource):
    type: Literal["foo"] = "foo"


class Bar(IncIdRessource):
    type: Literal["bar"] = "bar"


class RobotModel(IncIdRessource):
    type: Literal["robot"] = "robot"


Ressource = Annotated[
    Foo | Bar,
    Field(..., discriminator="type"),
]


class Transaction(BaseModel):
    ts: int  # timestamp in ms
    add: list[Ressource] = Field(default_factory=list, exclude=True)
    remove: list[Ressource] = Field(default_factory=list, exclude=True)

    def __init__(self, **kwargs):
        if "ts" not in kwargs:
            kwargs["ts"] = scheduler.ts
        super().__init__(**kwargs)
