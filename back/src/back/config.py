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

    port: int = 8080
    monitoring_port: int = 9000


class ApplicationConfig(CamelBaseModel):
    """Application configuration."""

    api: ApiConfig = ApiConfig()
