import pytest


@pytest.fixture
def default():
    return {
        'area': 25,
        'is_trees': False
    }


@pytest.fixture
def correct():
    return {
        'area': 35,
        'is_trees': True
    }
