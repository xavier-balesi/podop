from functools import partial

from back.config import ApplicationConfig, GameConfig
from back.controllers.robot import Robot
from back.models.ressources import Bar, Foo, FooBar, Money
from back.models.transaction import Transaction

game_config: GameConfig = ApplicationConfig().game


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
            Robot.build(inventory=self) for _ in range(game_config.min_robots)
        ]

    def __str__(self):
        return f"Inventory(foos={len(self.foos)}, bars={len(self.bars)}, foobars={len(self.foobars)}, robots={len(self.robots)}, money={self.money.value})"

    def get_ressource(self, ressource_name, lock=True) -> Foo | None:
        ressources = getattr(self, ressource_name + "s")
        for ressource in ressources:
            if ressource.lock:
                continue
            if lock:
                ressource.lock = True
            return ressource
        return None

    def get_foobars(self, count, lock=True) -> list[FooBar]:
        foobars = []
        for foobar in self.foobars:
            if foobar.lock:
                continue
            if lock:
                foobar.lock = True
            foobars.append(foobar)
            if len(foobars) == count:
                break

        # Revert the lock when the count is not there.
        if len(foobars) != count:
            for foobar in foobars:
                foobar.lock = False
            return []

        return foobars

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
                case Money():
                    self.money += model

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
                case Money():
                    self.money -= model
