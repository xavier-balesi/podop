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

    def transaction_handler(self, transaction: Transaction):
        self._transactions.append(transaction)

    def get_stats(self):
        return {"foo": "bar"}

    def start_next_turn(self):
        scheduler.tick()
