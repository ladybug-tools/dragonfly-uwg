import pytest


@pytest.fixture
def default():
    return {
        'albedo': 0.1,
        'thickness': 0.5,
        'conductivity': 1,
        'volumetric_heat_capacity': 1600000
    }


@pytest.fixture
def correct():
    return {
        'albedo': 0.5,
        'thickness': 0.3,
        'conductivity': 3,
        'volumetric_heat_capacity': 1700000
    }
