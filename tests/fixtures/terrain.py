import pytest


@pytest.fixture
def correct():
    return {
        'area': 25,
        'characteristic_length': 5
    }
