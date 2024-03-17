from unittest.mock import Mock

from back import Scheduler


def test_scheduler_schedule_on_correct_time():
    sched = Scheduler()
    task = Mock()

    sched.schedule(100, task, a=1, b=2)
    task.assert_not_called()

    sched.set_timestamp(99)
    task.assert_not_called()

    sched.set_timestamp(100)
    task.assert_called_once_with(a=1, b=2)


def test_scheduler_verify_order():
    sched = Scheduler()
    task1 = Mock()
    task2 = Mock()

    sched.schedule(100, task1)
    sched.schedule(200, task2)

    sched.set_timestamp(99)
    task1.assert_not_called()
    task2.assert_not_called()

    sched.set_timestamp(100)
    task1.assert_called_once()
    task2.assert_not_called()

    sched.set_timestamp(199)
    task1.assert_called_once()
    task2.assert_not_called()

    sched.set_timestamp(200)
    task1.assert_called_once()
    task2.assert_called_once()


def test_scheduler_verify_order_reverse():
    """Verify that only the delay has in influence, not the order we schedule tasks."""
    sched = Scheduler()
    task1 = Mock()
    task2 = Mock()

    sched.schedule(200, task2)
    sched.schedule(100, task1)

    sched.set_timestamp(99)
    task1.assert_not_called()
    task2.assert_not_called()

    sched.set_timestamp(100)
    task1.assert_called_once()
    task2.assert_not_called()

    sched.set_timestamp(199)
    task1.assert_called_once()
    task2.assert_not_called()

    sched.set_timestamp(200)
    task1.assert_called_once()
    task2.assert_called_once()
