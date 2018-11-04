from dragonfly.uwg.regionpar import BoundaryLayerPar
import pytest
from tests.fixtures.boundary_layer_parameters import default, correct


@pytest.mark.usefixtures("correct")
def test_initialise(correct):
    correct_parameters = BoundaryLayerPar(correct['day_boundary_layer_height'],
                                          correct['night_boundary_layer_height'],
                                          correct['inversion_height'],
                                          correct['circulation_coefficient'],
                                          correct['exchange_coefficient'])

    assert correct_parameters.day_boundary_layer_height == \
        correct['day_boundary_layer_height']
    assert correct_parameters.night_boundary_layer_height == \
        correct['night_boundary_layer_height']
    assert correct_parameters.inversion_height == \
        correct['inversion_height']
    assert correct_parameters.circulation_coefficient == \
        correct['circulation_coefficient']
    assert correct_parameters.exchange_coefficient == \
        correct['exchange_coefficient']


@pytest.mark.usefixtures("default")
def test_default(default):
    default_parameters = BoundaryLayerPar()

    assert default_parameters.day_boundary_layer_height == \
        default['day_boundary_layer_height']
    assert default_parameters.night_boundary_layer_height == \
        default['night_boundary_layer_height']
    assert default_parameters.inversion_height == \
        default['inversion_height']
    assert default_parameters.circulation_coefficient == \
        default['circulation_coefficient']
    assert default_parameters.exchange_coefficient == \
        default['exchange_coefficient']


def test_json(correct):
    parameters = BoundaryLayerPar(correct['day_boundary_layer_height'],
                                  correct['night_boundary_layer_height'],
                                  correct['inversion_height'],
                                  correct['circulation_coefficient'],
                                  correct['exchange_coefficient'])

    param_json = parameters.to_json()

    assert param_json == correct
    assert BoundaryLayerPar.from_json(param_json).to_json() == correct
