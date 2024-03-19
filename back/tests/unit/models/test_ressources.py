import pytest
from back.models.ressources import BaseRessource, Money


class TestBaseRessource:
    def test_init_subclass(self):
        with pytest.raises(TypeError):

            class TestRessource(BaseRessource):
                """Test class without discriminator."""


class TestMoney:
    def test_total_ordering(self):
        assert Money(value=1) == Money(value=1)
        assert Money(value=1) != Money(value=2)
        assert not Money(value=1) < Money(value=1)
        assert Money(value=1) < Money(value=2)
        assert not Money(value=2) < Money(value=2)
        assert Money(value=2) > Money(value=1)
        assert Money(value=1) <= Money(value=1)
        assert Money(value=1) <= Money(value=2)
        assert Money(value=2) >= Money(value=2)
        assert Money(value=2) >= Money(value=1)

    def test_total_ordering_with_int(self):
        assert Money(value=1) == 1
        assert Money(value=1) != 2
        assert not Money(value=1) < 1
        assert Money(value=1) < 2
        assert not Money(value=2) < 2
        assert Money(value=2) > 1
        assert Money(value=1) <= 1
        assert Money(value=1) <= 2
        assert Money(value=2) >= 2
        assert Money(value=2) >= 1

    def test_add_sub(self):
        money = Money(value=0)
        money += Money(value=1)
        money += 1
        money -= Money(value=1)
        money -= 1
