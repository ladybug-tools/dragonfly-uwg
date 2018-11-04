import pytest


@pytest.fixture
def correct():
    return {
        'average_height': 35,
        'footprint_area': 45,
        'facade_area': 33,
        'bldg_program': 'Hospital',
        'bldg_era': '1980sPresent',
        'floor_to_floor': 3,
        'glz_ratio': 0.3,
        'floor_area': 46,
        'number_of_stories': 5
    }


@pytest.fixture
def default():
    return {
        'average_height': 35,
        'footprint_area': 45,
        'facade_area': 33,
        'bldg_program': 'Hospital',
        'bldg_era': '1980sPresent',
        'floor_to_floor': 3.05,
        'glz_ratio': 0.1461,
        'floor_area': 225,
        'number_of_stories': 5
    }
