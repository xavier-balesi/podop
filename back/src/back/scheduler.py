import logging
from functools import partial
from heapq import heappop, heappush

log = logging.getLogger(__name__)


class Scheduler:
    """
    The game scheduler is not based on real timestamps, real delays, allowing for the scheduling of the next game turn
    directly after the previous one. Indeed, the primary objective of the game appears to be the construction of a
    trading model (using algorithms or machine learning), and the more parties we run, the better.
    """

    def __init__(self):
        self.ts = 0
        # heapq is not thread safe and then, more optimal than synchronisation queues (sync or async)
        self._tasks = []

    def scheduleabs(self, timestamp, action, *args, **kwargs):
        simplified_action = partial(action, *args, **kwargs)
        heappush(self._tasks, (timestamp, simplified_action))
        log.debug(
            f"scheduling at {timestamp} action {action} with args={args} and kwargs={kwargs}"
        )

    def schedule(self, delay, action, *args, **kwargs):
        ts = self.ts + delay
        self.scheduleabs(ts, action, *args, **kwargs)

    # def tick(self):
    #     self.set_timestamp(self.ts + 1)

    def set_timestamp(self, timestamp):
        log.debug(f"now at {timestamp}")
        self.ts = timestamp
        while self._tasks and (action_ts := self._tasks[0][0]) <= self.ts:
            log.debug(f"executing action planned for {action_ts}")
            _, action = heappop(self._tasks)
            action()

    def jump(self, delay):
        ts = self.ts + delay
        self.set_timestamp(ts)

    def reset(self):
        log.debug("resetting scheduler")
        self.ts = 0
        self._tasks[:] = []
