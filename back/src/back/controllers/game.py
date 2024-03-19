import asyncio
import logging

from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.controllers.player import RandomStrategyPlayer
from back.controllers.robot import Robot
from back.models.inventory import Inventory
from back.models.transaction import Transaction

game_config: GameConfig = ApplicationConfig().game
log = logging.getLogger()


class Game:
    __slots__ = ["_player", "_inventory", "running", "_transactions"]

    def __init__(self):
        self._player = RandomStrategyPlayer(game=self)
        self._inventory = Inventory()
        self.running: bool = True

        # Transactions are like "gold source" outputs of the game.
        # Declare fake transactions with initial robots just in case we want a reinforcement learning model
        # to understand the game initial state.
        self._transactions = [
            Transaction(add=[robot for robot in self._inventory.robots])
        ]
        # for txn in self._transactions:
        #     self.on_new_transaction(txn)

        for robot in self._inventory.robots:
            robot.subscribe(Transaction, self.on_new_transaction)

    def on_new_transaction(self, transaction: Transaction):
        self._transactions.append(transaction)

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
        if len(self._inventory.foos) >= 10000:
            self.running = False
            return

        # Once the inventory is updated, propose to the player to play, make orders.
        self._player.trade_in_live()

    def get_stats(self):
        inventory = self._inventory
        return {
            "foo": len(inventory.foos),
            "bar": len(inventory.bars),
            "foobar": len(inventory.foobars),
            "robot": len(inventory.robots),
            "money": inventory.money.value,
            "ts": scheduler.ts,
            "transaction": len(self._transactions),
        }

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
            # execute all tasks
            scheduler.set_timestamp(scheduler._tasks[-1].start_ts)
        else:
            log.critical("The game has deadlock... Aborting.")
            self.running = False
