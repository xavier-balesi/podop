from typing import Annotated

from pydantic import BaseModel, Field

from back import scheduler
from back.controllers.robot import Robot
from back.models.ressources import Bar, Foo, FooBar, Money

IncrIdRessources = Robot | Foo | Bar | FooBar
InventoryModel = Annotated[
    IncrIdRessources | Money,
    Field(..., discriminator="type"),
]


class Transaction(BaseModel):
    ts: int  # timestamp in ms
    add: list[InventoryModel] = Field(default_factory=list)
    remove: list[InventoryModel] = Field(default_factory=list)

    def __init__(self, **kwargs):
        if "ts" not in kwargs:
            kwargs["ts"] = scheduler.ts
        super().__init__(**kwargs)
