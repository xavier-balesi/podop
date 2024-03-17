import pytest
from back import scheduler
from back.models.transaction import Bar, Foo, RobotModel


@pytest.fixture(autouse=True)
def reset_game(request):
    for obj in (scheduler, Foo, Bar, RobotModel):
        obj.reset()
