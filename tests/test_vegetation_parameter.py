from dragonfly.uwg.districtpar import VegetationPar
import pytest
from tests.fixtures.vegetation_parameter import default, correct


def test_initialise(correct):
    correct_parameters = VegetationPar(correct['vegetation_albedo'],
                                       correct['vegetation_start_month'],
                                       correct['vegetation_end_month'],
                                       correct['tree_latent_fraction'],
                                       correct['grass_latent_fraction'])

    assert correct_parameters.vegetation_albedo == correct['vegetation_albedo']
    assert correct_parameters.vegetation_start_month == correct['vegetation_start_month']
    assert correct_parameters.vegetation_end_month == correct['vegetation_end_month']
    assert correct_parameters.tree_latent_fraction == correct['tree_latent_fraction']
    assert correct_parameters.grass_latent_fraction == correct['grass_latent_fraction']


def test_default(default):
    default_parameters = VegetationPar()

    assert default_parameters.vegetation_albedo == default['vegetation_albedo']
    assert default_parameters.vegetation_start_month == default['vegetation_start_month']
    assert default_parameters.vegetation_end_month == default['vegetation_end_month']
    assert default_parameters.tree_latent_fraction == default['tree_latent_fraction']
    assert default_parameters.grass_latent_fraction == default['grass_latent_fraction']


def test_json(correct):
    parameters = VegetationPar(correct['vegetation_albedo'],
                               correct['vegetation_start_month'],
                               correct['vegetation_end_month'],
                               correct['tree_latent_fraction'],
                               correct['grass_latent_fraction'])

    param_json = parameters.to_json()

    assert param_json == correct
    assert VegetationPar.from_json(param_json).to_json() == correct
