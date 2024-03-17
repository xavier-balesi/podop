from pydantic import BaseModel


class Money(BaseModel):
    value: int = 0  # in euros


class Warehouse:
    def __init__(self):
        self.money = Money()
        self.robots
