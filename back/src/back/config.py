import logging

from pydantic import BaseModel

log = logging.getLogger(__name__)


def to_lower_camel_case(string: str) -> str:
    """Return the lower camel case version of the input string as used in helmfiles."""
    tokens = string.split("_")
    return tokens[0] + "".join(token.capitalize() for token in tokens[1:])


class CamelBaseModel(BaseModel):
    """Base model class to use the lower camel case like the other config files in the helmfiles."""

    class Config:  # pylint: disable=missing-class-docstring
        alias_generator = to_lower_camel_case


class ApiConfig(CamelBaseModel):
    """HTTP servers configuration."""

    port: int = 8000
    monitoring_port: int = 9000
    framerate: int = (
        # Number of notification per second sent by the backend to the frontend.
        # Could be adapted according to the "turn_interval" parameter.
        30
    )


class GameConfig(CamelBaseModel):
    """Game configuration."""

    # Using ints to avoid float precision errors (using decimal module is less direct).
    move_duration: int = 5000  # in ms
    mine_foo_duration: int = 1000  # in ms
    mine_bar_duration_min: int = 500  # in ms
    mine_bar_duration_max: int = 2000  # in ms
    forge_foobar_duration: int = 2000  # in ms
    forge_foobar_success_rate: int = 60  # in percent
    sell_foobar_duration: int = 10000  # in ms
    sell_foobar_max_count: int = 5
    money_for_foobar: int = 1  # in euros
    buy_robot_duration: int = 0  # in ms
    money_for_robot: int = 3  # number of euros to buy a robot
    foo_for_robot: int = 6  # number of foo to buy a robot
    min_robots: int = 2  # the game starts with this number of robots
    max_robots: int = 30  # the game ends when reaching this number of robots
    turn_duration: int = (
        10  # duration of one turn in ms, the scheduler jump with this duration
    )
    turn_interval: int = (
        0  # interval between turns in ms, increase to slow down the game
    )


class ApplicationConfig(CamelBaseModel):
    """Application configuration."""

    api: ApiConfig = ApiConfig()
    game: GameConfig = GameConfig()
