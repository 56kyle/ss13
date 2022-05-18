
import pytest


@pytest.fixture(scope="session")
def map_file():
    with open('tests/data/map.dmm', 'r') as f:
        yield f
