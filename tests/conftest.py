import pytest


@pytest.fixture
def readDOE_file_path():
    return 'tests/resources/readDOE.pkl'


@pytest.fixture
def terrain_correct():
    return {
        'area': 25,
        'characteristic_length': 5
    }
