from abc import ABC, abstractmethod

from back.models.transaction import Transaction


class TransactionListener(ABC):
    @abstractmethod
    def on_new_transaction(self, transaction: Transaction) -> None:
        pass
