from dragonfly.vegetation import Vegetation
import pytest
from tests.fixtures.vegetation import correct, default


def test_initialise(correct):
    vegetation = Vegetation(correct['area'],
                            correct['is_trees'])

    assert vegetation.area == correct['area']
    assert vegetation.is_trees == correct['is_trees']


def test_default(default):
    vegetation = Vegetation(default['area'],
                            default['is_trees'])

    assert vegetation.area == default['area']
    assert vegetation.is_trees == default['is_trees']


def test_json(correct):
    vegetation = Vegetation(area=correct['area'],
                            is_trees=correct['is_trees'])

    terrain_json = vegetation.to_json()

    assert terrain_json == correct
    assert Vegetation.from_json(terrain_json).to_json() == correct
