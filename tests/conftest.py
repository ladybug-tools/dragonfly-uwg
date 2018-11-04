import pytest


@pytest.fixture
def terrain_correct():
    return {
        'area': 25,
        'characteristic_length': 5
    }
