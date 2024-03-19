import pytest
from back import scheduler
from back.controllers.robot import Robot
from back.models.ressources import Bar, Foo


@pytest.fixture(autouse=True)
def reset_game(request):
    for obj in (scheduler, Foo, Bar, Robot):
        obj.reset()
