from typing import Annotated

from pydantic import BaseModel, Field

from back import scheduler
from back.controllers.robot import Robot
from back.models.ressources import Bar, Foo, FooBar, Money

# Model = TypeVar("Model", bound=BaseModel)


# class EventType(StrEnum):
#     MINED = auto()
#
# Event = Annotated[
#     EnrichProcessor | RemoveProcessor | SetProcessor | ScriptProcessor,
#     Field(..., discriminator="type"),
# ]


InventoryModel = Annotated[
    Robot | Foo | Bar | FooBar | Money,
    Field(..., discriminator="type"),
]


class Transaction(BaseModel):
    ts: int  # timestamp in ms
    add: list[InventoryModel] = Field(default_factory=list, exclude=True)
    remove: list[InventoryModel] = Field(default_factory=list, exclude=True)

    def __init__(self, **kwargs):
        if "ts" not in kwargs:
            kwargs["ts"] = scheduler.ts
        super().__init__(**kwargs)
