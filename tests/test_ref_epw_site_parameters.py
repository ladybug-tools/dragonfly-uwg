from dragonfly.uwg.regionpar import RefEPWSitePar
import pytest
from tests.fixtures.ref_epw_site_parameter import correct, default


def test_initialise(correct):
    correct_parameters = RefEPWSitePar(correct['average_obstacle_height'],
                                       correct['vegetation_coverage'],
                                       correct['temp_measure_height'],
                                       correct['wind_measure_height'])

    assert correct_parameters.average_obstacle_height == \
        correct['average_obstacle_height']
    assert correct_parameters.vegetation_coverage == \
        correct['vegetation_coverage']
    assert correct_parameters.temp_measure_height == \
        correct['temp_measure_height']
    assert correct_parameters.wind_measure_height == \
        correct['wind_measure_height']


def test_default(default):
    default_parameters = RefEPWSitePar()

    assert default_parameters.average_obstacle_height == \
        default['average_obstacle_height']
    assert default_parameters.vegetation_coverage == \
        default['vegetation_coverage']
    assert default_parameters.temp_measure_height == \
        default['temp_measure_height']
    assert default_parameters.wind_measure_height == \
        default['wind_measure_height']


def test_json(correct):
    parameters = RefEPWSitePar(correct['average_obstacle_height'],
                               correct['vegetation_coverage'],
                               correct['temp_measure_height'],
                               correct['wind_measure_height'])

    param_json = parameters.to_json()

    assert param_json == correct
    assert RefEPWSitePar.from_json(param_json).to_json() == correct
