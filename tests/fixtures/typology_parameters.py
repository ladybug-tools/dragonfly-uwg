import pytest


@pytest.fixture
def correct():
    return {
        'fract_heat_to_canyon': 0.4,
        'shgc': 0.3,
        'wall_albedo': 0.4,
        'roof_albedo': 0.5,
        'roof_veg_fraction': 0.2,
    }


@pytest.fixture
def default():
    return {
        'fract_heat_to_canyon': 0.5,
        'shgc': None,
        'wall_albedo': None,
        'roof_albedo': None,
        'roof_veg_fraction': 0,
    }
