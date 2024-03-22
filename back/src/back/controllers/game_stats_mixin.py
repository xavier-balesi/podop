import logging

from back import scheduler
from back.controllers.trading_resource_game import TradingResourceGame
from back.models.counts_history import Counts, CountsHistory

log = logging.getLogger(__name__)


class GameStatsMixin(TradingResourceGame):
    def get_counts(self) -> Counts:
        inventory = self._inventory
        return Counts(  # type: ignore
            ts=scheduler.ts,
            foo=len(inventory.foos),
            bar=len(inventory.bars),
            foobar=len(inventory.foobars),
            robot=len(inventory.robots),
            money=inventory.money.value,
        )

    def get_counts_history(self) -> CountsHistory:
        counts_history: CountsHistory = CountsHistory()
        sorted_transactions = sorted(self._transactions, key=lambda t: t.ts)
        for transaction in sorted_transactions:
            if len(counts_history) == 0:
                new_counts = Counts(ts=0, foo=0, bar=0, foobar=0, robot=0, money=0)  # type: ignore
                new_counts.update(transaction)
                counts_history.append(new_counts)
            else:
                last_counts = counts_history[-1]
                new_counts = last_counts.model_copy(deep=True)
                new_counts.update(transaction)
                assert new_counts.ts == transaction.ts
                if last_counts.ts == new_counts.ts:
                    counts_history[-1] = new_counts
                else:
                    counts_history.append(new_counts)
        return counts_history
