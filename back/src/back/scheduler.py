import logging
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import partial, wraps
from heapq import heappop, heappush

log = logging.getLogger(__name__)


@dataclass(order=True)
class Task:
    start_ts: int  # in ms
    action: Callable[[], None] = field(compare=False)


class Scheduler:
    """The game scheduler is not based on real timestamps, real delays, allowing for the scheduling of the next game turn
    directly after the previous one. Indeed, the primary objective of the game appears to be the construction of a
    trading model (using algorithms or machine learning), and the more parties we run, the better.
    """

    __slots__ = ["ts", "_tasks"]

    def __init__(self) -> None:
        self.ts = 0
        # heapq is not thread safe and then, more optimal than synchronisation queues (sync or async)
        self._tasks = []

    def scheduleabs(self, timestamp, action, *args, **kwargs) -> None:
        simplified_action = partial(action, *args, **kwargs)
        heappush(self._tasks, Task(start_ts=timestamp, action=simplified_action))
        log.debug(
            f"scheduling at {timestamp} action {action} with args={args} and kwargs={kwargs}",
        )

    def schedule(self, delay, action, *args, **kwargs) -> None:
        ts = self.ts + delay
        self.scheduleabs(ts, action, *args, **kwargs)

    def set_timestamp(self, timestamp) -> None:
        # log.debug(f"now at {timestamp}")
        self.ts = timestamp
        while self._tasks and (action_ts := self._tasks[0].start_ts) <= self.ts:
            log.debug(f"executing action planned for {action_ts}")
            task: Task = heappop(self._tasks)
            task.action()

    def jump(self, delay) -> None:
        ts = self.ts + delay
        self.set_timestamp(ts)

    def reset(self) -> None:
        log.debug("resetting scheduler")
        self.ts = 0
        self._tasks[:] = []

    @contextmanager
    def from_timestamp_contextmanager(self, ts):
        """Permit to change the now timestamp with a contextmanager.
        so that child schedules do not depend on future time shifting.
        """
        orig_ts = self.ts
        # change now timestamp
        self.ts = ts
        try:
            yield
        finally:
            # restore now timestamp
            self.ts = orig_ts

    def from_timestamp_decorator(self, ts):
        """Permit to change the now timestamp with a decorator
        so that child schedules do not depend on future time shifting.
        """

        def _from_timestamp_decorator(f):
            @wraps(f)
            def _from_timestamp_wrapper(*args, **kwargs):
                with self.from_timestamp_contextmanager(ts):
                    return f(*args, **kwargs)

            return _from_timestamp_wrapper

        return _from_timestamp_decorator

    @property
    def busy_until(self) -> int | None:
        return self._tasks[-1].start_ts if self._tasks else None
