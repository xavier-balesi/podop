class GameError(Exception):
    """Base class for Foobartory exceptions."""


class RobotBusyError(GameError):
    """The robot cannot do anything for now."""


class SellError(GameError):
    """Error while selling foobars."""
