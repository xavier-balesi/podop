from back.controllers.game_stats_mixin import GameStatsMixin
from back.models.counts_history import Counts, CountsHistory
from back.models.ressources import Foo, Money
from back.models.transaction import Transaction


class TestGameStatsMixin:
    def test_game_stats_mixin_on_new_transaction(self):
        mixin = GameStatsMixin()
        mixin.on_new_transaction(
            Transaction(ts=1, add=[Foo.build()], remove=[Money(value=2)]),
        )
        counts_history = mixin.get_counts_history()
        expected_counts = Counts(ts=1, foo=1, bar=0, foobar=0, robot=0, money=-2)
        expected_history = CountsHistory([expected_counts])
        assert counts_history == expected_history
        assert counts_history[0:] == expected_history
        assert counts_history[0] == expected_counts
