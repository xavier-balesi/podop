import logging
from functools import partial
from random import choice, randint
from typing import TYPE_CHECKING

from back.config import ApplicationConfig, GameConfig
from back.controllers.robot import Action

if TYPE_CHECKING:
    from back.controllers.game import Game

game_config: GameConfig = ApplicationConfig().game
log = logging.getLogger(__name__)


class Player:
    """Mining gamer or trader, that is the question."""


class RandomStrategyPlayer(Player):
    """Player that plays randomly.
    Many random games might help finding good strategies.
    """

    __slots__ = ["_game"]

    def __init__(self, game: "Game") -> None:
        self._game: Game | None = game

    def destroy(self) -> None:
        """Destructor method.

        Not using __del__ because it notifies when the object is garbage collected,
        but it may not be called with cyclic references. It's not deterministic, so it's not
        compatible to avoid memory leaks.
        In cpython, __del__ is in practice called when there is no more reference to the object,
        but with PyPy it's delayed for performances.
        """
        self._game = None

    def trade_in_live(self) -> None:
        """Play each time the game changes."""
        if (game := self._game) is None:
            log.warning("The game is detached fom the player.")
            return
        inventory = game.get_inventory()
        for robot in inventory.robots:
            if robot.action != Action.WAITING_FOR_ORDER:
                continue

            # It's always possible to mine foo or bar.
            possible_actions = [robot.mine_foo, robot.mine_bar]

            # Can we forge a foobar?
            if inventory.get_foo(lock=False) and inventory.get_bar(lock=False):  # type: ignore
                possible_actions.append(robot.forge_foobar)

            # Can we sell a random count of foobar?
            sell_count = randint(1, game_config.sell_foobar_max_count)
            if inventory.get_foobars(count=sell_count, lock=False):  # type: ignore
                possible_actions.append(partial(robot.sell_foobar, count=sell_count))

            # Can we buy a robot?
            if inventory.money >= game_config.money_for_robot and inventory.get_foos(  # type: ignore
                count=game_config.foo_for_robot,
                lock=False,
            ):
                possible_actions.append(robot.buy_robot)

            # Choose a random action that respect game rules.
            random_action = choice(possible_actions)
            log.debug(f"player choose {random_action} while {game.get_counts()}")
            random_action()
