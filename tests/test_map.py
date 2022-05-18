import pytest

from ss13.map import Map


def test_map_init(map_file):
    map = Map(map_file)
    assert map.coords.shape[0] == map.coords.shape[1]

