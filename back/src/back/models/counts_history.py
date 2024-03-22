from collections import Counter

from pydantic import Field, RootModel

from back.models.ressources import Money
from back.models.transaction import Transaction

# class Counts(BaseModel):
#     ts: int
#     foo: int
#     bar: int
#     foobar: int
#     robot: int
#     money: int
#
#     def update(self, transaction: Transaction):
#         for add in transaction.add:
#             self[add.type] += 1
#         for remove in transaction.remove:
#             self[remove.type] -= 1


class Counts(RootModel):
    root: Counter

    def update(self, transaction: Transaction):
        root = self.root
        root["ts"] = transaction.ts
        for add in transaction.add:
            root[add.type] += add.value if type(add) is Money else 1
        for remove in transaction.remove:
            root[remove.type] -= remove.value if type(remove) is Money else 1

    @property
    def ts(self):
        return self.root["ts"]


class CountsHistory(RootModel):
    root: list[Counts] = Field(default_factory=list)

    def append(self, counts: Counts):
        self.root.append(counts)

    def __len__(self):
        return len(self.root)

    def __getitem__(self, key):
        if type(key) is slice:
            return type(self)(self.root[key])
        return self.root[key]

    def __setitem__(self, key, value):
        self.root[key] = value
