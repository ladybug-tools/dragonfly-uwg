from dragonfly.dfparameter import PavementPar
import pytest
from tests.fixtures.pavement_parameter import correct, default


def test_initialise(correct):
    correct_parameters = PavementPar(correct['albedo'],
                                     correct['thickness'],
                                     correct['conductivity'],
                                     correct['volumetric_heat_capacity'])

    assert correct_parameters.albedo == correct['albedo']
    assert correct_parameters.thickness == correct['thickness']
    assert correct_parameters.conductivity == correct['conductivity']
    assert correct_parameters.volumetric_heat_capacity == correct['volumetric_heat_capacity']


def test_default(default):
    default_parameters = PavementPar()

    assert default_parameters.albedo == default['albedo']
    assert default_parameters.thickness == default['thickness']
    assert default_parameters.conductivity == default['conductivity']
    assert default_parameters.volumetric_heat_capacity == default['volumetric_heat_capacity']
