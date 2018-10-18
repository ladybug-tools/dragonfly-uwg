from dragonfly.terrain import Terrain
import pytest
from tests.fixtures.terrain import correct


def test_initialise(correct):
    terrain = Terrain(correct['area'])

    assert terrain.area == correct['area']
    assert terrain.characteristic_length == correct['characteristic_length']

    forced_length = Terrain(24, 4)

    assert forced_length.area == 24
    assert forced_length.characteristic_length == 4
