import asyncio
import logging

from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.controllers.game_stats_mixin import GameStatsMixin
from back.controllers.player import RandomStrategyPlayer
from back.controllers.robot import Robot
from back.controllers.trading_resource_game import TradingResourceGame
from back.models.transaction import Transaction

game_config: GameConfig = ApplicationConfig().game
log = logging.getLogger()


class Game(GameStatsMixin, TradingResourceGame):
    __slots__ = ["_player", "_inventory", "running", "_transactions"]

    def __init__(self):
        super().__init__()

        self._player = RandomStrategyPlayer(game=self)

        # Declare fake transactions with initial robots just in case we want a reinforcement learning model
        # to understand the game initial state.
        self._transactions.extend(
            [Transaction(add=[robot for robot in self._inventory.robots])]
        )
        super().on_new_transaction(self._transactions[0])

        # Observe initial robots.
        for robot in self._inventory.robots:
            robot.subscribe(Transaction, self.on_new_transaction)

    def on_new_transaction(self, transaction: Transaction) -> None:
        super().on_new_transaction(transaction)

        # Observe new robots.
        for model in transaction.add:
            match model:
                case Robot():
                    model.subscribe(Transaction, self.on_new_transaction)
        for model in transaction.remove:
            match model:
                case Robot():
                    model.unsubscribe(Transaction, self.on_new_transaction)

        # Control when the inventory gets updated.
        self._inventory.on_new_transaction(transaction)

        # Eventually stop the game.
        if len(self._inventory.robots) >= game_config.max_robots:
            self.running = False
            return

        # Once the inventory is updated, propose to the player to play, make orders.
        self._player.trade_in_live()

    async def run(self):
        # player plays for the first time
        self._player.trade_in_live()

        while self.running:
            self.start_next_turn()
            # Even if turn_interval=0, we need to wait to not block the main asyncio loop and
            # to abort the program on Ctrl+C.
            await asyncio.sleep(game_config.turn_interval / 1000)

    def start_next_turn(self):
        if scheduler._tasks:
            # Execute all tasks by jumping to the last task timestamp.
            scheduler.set_timestamp(scheduler._tasks[-1].start_ts)
        else:
            log.critical("⛔ The game has deadlock... Aborting.")
            self.running = False
