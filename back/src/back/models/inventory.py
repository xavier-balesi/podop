from functools import partial

from pydantic import BaseModel

from back.config import ApplicationConfig, GameConfig
from back.controllers.robot import Robot
from back.models.ressources import Bar, Foo, FooBar
from back.models.transaction import Transaction

game_config: GameConfig = ApplicationConfig().game


class Money(BaseModel):
    value: int = 0  # in euros


class Inventory:
    """
    Inventory of all game data models.
    Act as the :class:`~back.controllers.Game` data model.
    """

    def __init__(self):
        # Complete class methods.
        for ressource_name in ("foo", "bar", "foobar", "robot"):
            setattr(
                self,
                "get_" + ressource_name,
                partial(self.get_ressource, ressource_name),
            )

        # Populate the inventory with default values.
        self.money = Money()
        self.foos: list[Foo] = []
        self.bars: list[Bar] = []
        self.foobars: list[FooBar] = []
        self.robots: list[Robot] = [
            Robot(inventory=self) for _ in range(game_config.min_robots)
        ]

    def get_ressource(self, ressource_name, lock=True) -> Foo | None:
        ressources = getattr(self, ressource_name + "s")
        for ressource in ressources:
            if not ressource.lock:
                if lock:
                    ressource.lock = True
                return ressource
        return None

    def on_new_transaction(self, transaction: Transaction):
        for model in transaction.add:
            match model:
                case Foo():
                    self.foos.append(model)
                case Bar():
                    self.bars.append(model)
                case FooBar():
                    self.foobars.append(model)
                case Robot():
                    self.robots.append(model)

        for model in transaction.remove:
            match model:
                case Foo():
                    self.foos.remove(model)
                case Bar():
                    self.bars.remove(model)
                case FooBar():
                    self.foobars.remove(model)
                case Robot():
                    self.robots.remove(model)
