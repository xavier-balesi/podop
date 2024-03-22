from back.models.inventory import Inventory
from back.models.transaction import Transaction


class TradingResourceGame:
    """
    Interface for a trading resource game.

    NB: Trading resources generates transactions.
    """

    def __init__(self):
        super().__init__()
        self._inventory: Inventory = Inventory()
        self.running: bool = True

        # Transactions are like "gold source" outputs of the game.
        self._transactions: list[Transaction] = []

    def on_new_transaction(self, transaction: Transaction) -> None:
        """The game is notified when a transaction of resources happens."""
        self._transactions.append(transaction)
