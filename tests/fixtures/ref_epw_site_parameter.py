import pytest


@pytest.fixture
def default():
    return {
        'average_obstacle_height': 0.1,
        'vegetation_coverage': 0.9,
        'temp_measure_height': 10,
        'wind_measure_height': 10
    }


@pytest.fixture
def correct():
    return {
        'average_obstacle_height': 0.5,
        'vegetation_coverage': 0.3,
        'temp_measure_height': 15,
        'wind_measure_height': 12
    }
