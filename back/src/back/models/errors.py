class GameError(Exception):
    """Base class for Foobartory exceptions."""


class RobotBusyError(GameError):
    """The robot cannot do anything for now."""


class InsufficientRessourceError(GameError):
    """Missing ressources to complete the task."""
