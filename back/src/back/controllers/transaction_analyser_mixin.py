from back.controllers.transaction_listener import TransactionListener
from back.models.counts_history import Counts, CountsHistory
from back.models.transaction import Transaction


class TransactionAnalyserMixin(TransactionListener):
    def __init__(self):
        self._counts_history: CountsHistory = CountsHistory()

    def on_new_transaction(self, transaction: Transaction):
        super().on_new_transaction(transaction)
        if len(self._counts_history) == 0:
            new_counts = Counts(ts=0, foo=0, bar=0, foobar=0, robot=0, money=0)
            new_counts.update(transaction)
            self._counts_history.append(new_counts)
        else:
            last_counts = self._counts_history[-1]
            new_counts = last_counts.model_copy(deep=True)
            new_counts.update(transaction)
            assert new_counts.ts == transaction.ts
            if last_counts.ts == new_counts.ts:
                self._counts_history[-1] = new_counts
            elif last_counts.ts > new_counts.ts:
                # TODO:
                #     debug scheduler behavior
                #   or update many counts objects starting from the end
                #     and eventually insert the new count at the correct position
                #     and return the index to update the chart from this past position
                #   or update all points based on all Transactions instead
                #     of optimizing
                pass
            else:
                self._counts_history.append(new_counts)

    def get_counts_history(self):
        return self._counts_history
