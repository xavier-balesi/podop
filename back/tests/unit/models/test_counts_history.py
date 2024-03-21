from back.models.counts_history import Counts
from back.models.ressources import Foo, Money
from back.models.transaction import Transaction


class TestCounts:
    def test_counts_update(self):
        counts = Counts(ts=0, foo=1, bar=2, foobar=3, robot=4, money=5)
        counts.update(Transaction(ts=1, add=[Foo.build()], remove=[Money(value=2)]))
        assert counts == Counts(ts=1, foo=2, bar=2, foobar=3, robot=4, money=3)

    def test_counts_serialization(self):
        counts = Counts(ts=0, foo=1, bar=2, foobar=3, robot=4, money=5)
        assert counts.dict() == {
            "ts": 0,
            "foo": 1,
            "bar": 2,
            "foobar": 3,
            "robot": 4,
            "money": 5,
        }
