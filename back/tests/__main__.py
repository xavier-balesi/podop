import faulthandler
import signal
import sys

import pytest

if __name__ == "__main__":
    # display traceback of all threads during tests with:
    # kill -SIGUSR1 $(pgrep -f tests/main.py)
    faulthandler.register(signal.SIGUSR1)

    exit(pytest.main(["--disable-warnings"] + sys.argv[1:]))
