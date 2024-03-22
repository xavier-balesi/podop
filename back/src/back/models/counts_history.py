from collections import Counter

from pydantic import Field, RootModel

from back.models.ressources import Money
from back.models.transaction import Transaction


class Counts(RootModel):
    root: Counter

    def update(self, transaction: Transaction) -> None:
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

    def append(self, counts: Counts) -> None:
        self.root.append(counts)

    def __len__(self) -> int:
        return len(self.root)

    def __getitem__(self, key):
        if type(key) is slice:
            return type(self)(self.root[key])
        return self.root[key]

    def __setitem__(self, key, value) -> None:
        self.root[key] = value
