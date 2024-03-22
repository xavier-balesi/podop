from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from back.models.transaction import Transaction

    # We could add other event types in the future.
    EventType = Transaction


class Provider:
    """Implementation of the Publish-Subscribe conversation pattern."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._observers: dict[
            type["EventType"],
            list[Callable[["EventType"], None]],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type["EventType"],
        handler: Callable[["EventType"], None],
    ) -> None:
        self._observers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: type["EventType"],
        handler: Callable[["EventType"], None],
    ) -> None:
        self._observers[event_type].remove(handler)

    def _publish(self, event: "EventType") -> None:
        for handler in self._observers[type(event)]:
            handler(event)
