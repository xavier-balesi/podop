import pytest

import tests.fixtures
from tests.lib.pytest import import_fixtures
from tests.lib.pytest.marker import add_skip_markers

add_skip_markers("wip", global_vars=globals())


def pytest_configure(config: pytest.Config):
    import_fixtures(tests.fixtures, globals())
