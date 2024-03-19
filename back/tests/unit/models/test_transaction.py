from copy import deepcopy
from typing import ClassVar

import pytest
from back.controllers.robot import Robot
from back.models.inventory import Inventory
from back.models.ressources import FooBar, Money
from back.models.transaction import Transaction


@pytest.fixture()
def txn():
    return Transaction(
        add=[Money(value=3), Robot(id=3, inventory=Inventory())],
        remove=[FooBar(id=0, foo_id=0, bar_id=0)],
    )


class TestTransaction:
    json_txn: ClassVar = {
        "ts": 0,
        "add": [{"type": "money", "value": 3}, {"type": "robot", "id": 3}],
        "remove": [{"type": "foobar", "id": 0, "foo_id": 0, "bar_id": 0}],
    }

    def test_serialize(self, txn):
        assert txn.dict() == self.json_txn

    def test_deserialize(self, txn):
        json_txn = deepcopy(self.json_txn)
        json_txn["add"][1]["inventory"] = Inventory()
        assert Transaction.parse_obj(json_txn).dict() == self.json_txn
