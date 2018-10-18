import pytest


@pytest.fixture
def correct():
    return {
        'average_height': 35,
        'footprint_area': 45,
        'facade_area': 33,
        'bldg_program': 'Hospital',
        'bldg_age': '1980sPresent',
        'floor_to_floor': 3,
        'fract_heat_to_canyon': 0.2,
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
        'bldg_age': '1980sPresent',
        'floor_to_floor': 3.05,
        'fract_heat_to_canyon': 0.5,
        'glz_ratio': 0.3,  # TODO: Determine default glz ration for 1980s Hostpital
        'floor_area': 48,  # TODO: Determine autocalculate value based on footprint area average height and floor to floor
        'number_of_stories': 5
    }
