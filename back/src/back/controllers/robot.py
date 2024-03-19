import logging
from enum import StrEnum, auto
from functools import wraps
from random import randint
from typing import TYPE_CHECKING, Literal

from pydantic import Field

from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.models.errors import RobotBusyError
from back.models.ressources import Bar, Foo, FooBar, IncIdRessource
from back.patterns.publish_subscribe import Provider

log = logging.getLogger(__name__)
game_config: GameConfig = ApplicationConfig().game
if TYPE_CHECKING:
    from back.models.inventory import Inventory


class Action(StrEnum):
    WAITING_FOR_ORDER = auto()
    MOVING = auto()
    MINE_FOO = auto()
    MINE_BAR = auto()
    FORGE_FOOBAR = auto()
    SELL_FOOBAR = auto()
    BUY_ROBOT = auto()


def action_wrapper(f):
    @wraps(f)
    def _action_wrapper(self, *args, **kwargs):
        if self.action != Action.WAITING_FOR_ORDER:
            raise RobotBusyError(
                f"Robot {self} can't {f.__name__} because it is not waiting for an order."
            )

        # Robot is at the good place, no need to move.
        if self.previous_action.name.lower() == f.__name__:
            return f(self, *args, **kwargs)

        # The robot have to move before executing the action.
        self.action = Action.MOVING
        after_moving_ts = scheduler.ts + game_config.move_duration
        scheduler.schedule(
            game_config.move_duration,
            # Future "child" schedules have to be executed directly after the move
            # and not depend on future time shifting.
            scheduler.from_timestamp_decorator(after_moving_ts)(f),
            self,
            *args,
            **kwargs,
        )
        return None

    return _action_wrapper


class Robot(Provider, IncIdRessource):
    type: Literal["robot"] = "robot"
    previous_action: Action = Field(default=Action.WAITING_FOR_ORDER, exclude=True)

    def __init__(self, inventory: "Inventory", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inventory = inventory
        self._action: Action = Action.WAITING_FOR_ORDER

    def _notify_transaction(self, *args, **kwargs):
        from back.models.transaction import Transaction

        self.action = Action.WAITING_FOR_ORDER
        self._publish(Transaction(*args, **kwargs))

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self.previous_action = self._action
        self._action = value
        log.debug(f"🤖 N°{self.id}: {self.previous_action} -> {self._action}")

    @action_wrapper
    def mine_foo(self):
        self.action = Action.MINE_FOO
        scheduler.schedule(game_config.mine_foo_duration, self._mine_foo_callback)

    def _mine_foo_callback(self):
        self._notify_transaction(add=[Foo.build()])

    @action_wrapper
    def mine_bar(self):
        self.action = Action.MINE_BAR
        mine_bar_duration = randint(
            game_config.mine_bar_duration_min, game_config.mine_bar_duration_max
        )
        scheduler.schedule(mine_bar_duration, self._mine_bar_callback)

    def _mine_bar_callback(self):
        self._notify_transaction(add=[Bar.build()])

    @action_wrapper
    def forge_foobar(self):
        self.action = Action.FORGE_FOOBAR
        inventory = self._inventory
        if not (foo := inventory.get_foo()):
            log.warning(f"🤖 N°{self.id}: not enough foo to forge a foobar")
            self.action = Action.WAITING_FOR_ORDER
            return
        if not (bar := inventory.get_bar()):
            log.warning(f"🤖 N°{self.id}: not enough bar to forge a foobar")
            foo.lock = False
            self.action = Action.WAITING_FOR_ORDER
            return

        scheduler.schedule(
            game_config.forge_foobar_duration,
            self._forge_foobar_callback,
            foo=foo,
            bar=bar,
        )

    def _forge_foobar_callback(self, foo, bar):
        random = randint(1, 100)
        if random <= game_config.forge_foobar_success_rate:
            self._notify_transaction(
                add=[FooBar.build(foo_id=foo.id, bar_id=bar.id)], remove=[foo, bar]
            )
        else:
            self._notify_transaction(remove=[foo])
            bar.lock = False
