import pytest


@pytest.fixture
def default():
    return {
        'day_boundary_layer_height': 1000,
        'night_boundary_layer_height': 80,
        'inversion_height': 150,
        'circulation_coefficient': 1.2,
        'exchange_coefficient': 1,
    }


@pytest.fixture
def correct():
    return {
        'day_boundary_layer_height': 2000,
        'night_boundary_layer_height': 82,
        'inversion_height': 153,
        'circulation_coefficient': 3.2,
        'exchange_coefficient': 4,
    }
