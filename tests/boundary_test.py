# coding=utf-8
from dragonfly_uwg.simulation.boundary import BoundaryLayerParameter

from tests.fixtures.boundary import default_boundary, custom_boundary


def test_boundary():
    """Test the existence of basic properties."""
    boundary = default_boundary()

    str(boundary)  # test the string representation
    assert boundary.day_boundary_layer_height == 1000
    assert boundary.night_boundary_layer_height == 80
    assert boundary.inversion_height == 150
    assert boundary.circulation_coefficient == 1.2
    assert boundary.exchange_coefficient == 1.0


def test_duplicate():
    """Test the duplicate method."""
    boundary = custom_boundary()
    new_boundary = boundary.duplicate()
    assert new_boundary is not boundary

    assert new_boundary.day_boundary_layer_height == boundary.day_boundary_layer_height
    assert new_boundary.night_boundary_layer_height == boundary.night_boundary_layer_height
    assert new_boundary.inversion_height == boundary.inversion_height
    assert new_boundary.circulation_coefficient == boundary.circulation_coefficient
    assert new_boundary.exchange_coefficient == boundary.exchange_coefficient


def test_to_from_dict():
    """Test the VegetationPararameter to_dict and from_dict methods."""
    boundary = custom_boundary()
    boundary_dict = boundary.to_dict()
    new_boundary = BoundaryLayerParameter.from_dict(boundary_dict)

    assert new_boundary.day_boundary_layer_height == boundary.day_boundary_layer_height
    assert new_boundary.night_boundary_layer_height == boundary.night_boundary_layer_height
    assert new_boundary.inversion_height == boundary.inversion_height
    assert new_boundary.circulation_coefficient == boundary.circulation_coefficient
    assert new_boundary.exchange_coefficient == boundary.exchange_coefficient
