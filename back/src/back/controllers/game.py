import asyncio
from collections import Counter

from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.controllers.player import Player
from back.controllers.robot import Robot
from back.models.transaction import Transaction

game_config: GameConfig = ApplicationConfig().game


class Game:
    def __init__(self):
        min_robots = game_config.min_robots
        self._player = Player(game=self)
        self._robots = [
            Robot(transaction_handler=self.transaction_handler)
            for _ in range(min_robots)
        ]
        self._transactions = [Transaction(add=[robot._model for robot in self._robots])]
        self.running: bool = True

        self._stats = Counter(foo=0, bar=0, robot=0)
        for transaction in self._transactions:
            self._update_stats(transaction)

    def transaction_handler(self, transaction: Transaction):
        self._transactions.append(transaction)
        self._update_stats(transaction)
        if self._stats["foo"] >= 10000:
            self.running = False
            return
        self._player.trade_in_live()

    def _update_stats(self, transaction: Transaction):
        stats = self._stats
        for add in transaction.add:
            stats[add.type] += 1
        for remove in transaction.remove:
            stats[remove.type] -= 1

    def get_stats(self):
        return self._stats

    async def run(self):
        # player plays for the first time
        self._player.trade_in_live()

        while self.running:
            self.start_next_turn()
            # Even if turn_interval=0, we need to wait to not block the main asyncio loop and
            # to abort the program on Ctrl+C.
            await asyncio.sleep(game_config.turn_interval / 1000)

    def start_next_turn(self):
        if not scheduler._tasks:
            assert False, "There is always tasks created by former ones"  # noqa: PT015
        # execute all tasks
        scheduler.set_timestamp(scheduler._tasks[-1].start_ts)
