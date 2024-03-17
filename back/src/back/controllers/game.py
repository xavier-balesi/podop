import asyncio

from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.controllers.player import Player
from back.controllers.robot import Robot
from back.models.transaction import Transaction

game_config: GameConfig = ApplicationConfig().game


class Game:
    def __init__(self):
        self._player = Player()
        self._transactions = []
        min_robots = game_config.min_robots
        self._robots = [
            Robot(transaction_handler=self.transaction_handler)
            for _ in range(min_robots)
        ]
        self.running: bool = True

    def transaction_handler(self, transaction: Transaction):
        self._transactions.append(transaction)

    def get_stats(self):
        return {"foo": "bar"}

    async def run(self):
        while self.running:
            self.start_next_turn()
            await asyncio.sleep(game_config.turn_interval)

    def start_next_turn(self):
        # TODO: intelligent jump to next time a robot is available
        scheduler.jump(game_config.turn_duration)
