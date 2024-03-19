from random import choice
from typing import TYPE_CHECKING

from back.controllers.robot import Action

if TYPE_CHECKING:
    from back.controllers.game import Game


class Player:
    """Mining gamer or trader, that is the question."""

    def __init__(self, game: "Game"):
        self._game = game

    def destroy(self):
        """
        Destructor method.

        Not using __del__ because it notifies when the object is garbage collected,
        but it may not be called with cyclic references. It's not deterministic, so it's not
        compatible to avoid memory leaks.
        In cpython, __del__ is in practice called when there is no more reference to the object,
        but with PyPy it's delayed for performances.
        """
        self._game = None

    def trade_in_live(self):
        """Play each time the game changes."""
        inventory = self._game._inventory
        for robot in inventory.robots:
            if robot.action != Action.WAITING_FOR_ORDER:
                continue
            possible_actions = [robot.mine_foo, robot.mine_bar]
            if inventory.foos and inventory.bars:
                possible_actions.append(robot.forge_foobar)
            random_action = choice(possible_actions)
            random_action()
