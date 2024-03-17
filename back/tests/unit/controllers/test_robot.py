from unittest.mock import Mock

import pytest
from back import scheduler
from back.config import ApplicationConfig, GameConfig
from back.controllers.robot import Robot
from back.models.errors import RobotBusyError
from back.models.transaction import Foo, Transaction


def test_robot_mine_foo():
    game_config: GameConfig = ApplicationConfig().game
    expected_minded_ts = (
        scheduler.ts + game_config.move_duration + game_config.mine_foo_duration
    )

    txn_handler = Mock()
    robot = Robot(transaction_handler=txn_handler)
    robot.mine_foo()
    scheduler.set_timestamp(scheduler.ts + game_config.move_duration)

    scheduler.set_timestamp(expected_minded_ts - 1)
    txn_handler.assert_not_called()

    scheduler.set_timestamp(expected_minded_ts)
    txn_handler.assert_called_once_with(
        Transaction(ts=expected_minded_ts, add=[Foo(id=0)])
    )


def test_robot_chain_mine_foo():
    game_config: GameConfig = ApplicationConfig().game
    expected_minded_ts = (
        scheduler.ts + game_config.move_duration + game_config.mine_foo_duration
    )

    txn_handler = Mock()
    robot = Robot(transaction_handler=txn_handler)
    robot.mine_foo()
    scheduler.jump(game_config.move_duration - 1)

    with pytest.raises(RobotBusyError):
        robot.mine_foo()

    txn_handler.assert_not_called()
    scheduler.jump(1 + game_config.mine_foo_duration)
    txn_handler.assert_called_once_with(
        Transaction(ts=expected_minded_ts, add=[Foo(id=0)])
    )

    robot.mine_foo()
    scheduler.jump(game_config.mine_foo_duration)
    txn_handler.assert_called_with(
        Transaction(
            ts=expected_minded_ts + game_config.mine_foo_duration, add=[Foo(id=1)]
        ),
    )
