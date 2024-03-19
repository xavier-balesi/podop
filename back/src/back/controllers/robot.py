import logging
from enum import StrEnum, auto
from functools import wraps
from random import randint
from typing import Callable

from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.models.errors import RobotBusyError
from back.models.transaction import Bar, Foo, RobotModel, Transaction

log = logging.getLogger(__name__)
game_config: GameConfig = ApplicationConfig().game


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
        if self._previous_action.name.lower() == f.__name__:
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


class Robot:
    def __init__(self, transaction_handler: Callable[[Transaction], None]):
        self._model: RobotModel = RobotModel.build()
        self._previous_action: Action = Action.WAITING_FOR_ORDER
        self._action: Action = Action.WAITING_FOR_ORDER
        self._transaction_handler = transaction_handler

    def _notify_transaction(self, *args, **kwargs):
        self.action = Action.WAITING_FOR_ORDER
        self._transaction_handler(*args, **kwargs)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._previous_action = self._action
        self._action = value
        log.debug(f"🤖 N°{self._model.id}: {self._previous_action} -> {self._action}")

    @action_wrapper
    def mine_foo(self):
        self.action = Action.MINE_FOO
        scheduler.schedule(game_config.mine_foo_duration, self._mine_foo_callback)

    def _mine_foo_callback(self):
        self._notify_transaction(Transaction(add=[Foo.build()]))

    @action_wrapper
    def mine_bar(self):
        self.action = Action.MINE_BAR
        mine_bar_duration = randint(
            game_config.mine_bar_duration_min, game_config.mine_bar_duration_max
        )
        scheduler.schedule(mine_bar_duration, self._mine_bar_callback)

    def _mine_bar_callback(self):
        self._notify_transaction(Transaction(add=[Bar.build()]))
