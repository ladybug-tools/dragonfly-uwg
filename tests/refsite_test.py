# coding=utf-8
from dragonfly_uwg.simulation.refsite import ReferenceEPWSite

from tests.fixtures.refsite import default_refsite, custom_refsite


def test_refsite():
    """Test the existence of basic properties."""
    refsite = default_refsite()

    str(refsite)  # test the string representation
    assert refsite.average_obstacle_height == 0.1
    assert refsite.vegetation_coverage == 0.9
    assert refsite.temp_measure_height == 10
    assert refsite.wind_measure_height == 10


def test_duplicate():
    """Test the duplicate method."""
    refsite = custom_refsite()
    new_refsite = refsite.duplicate()
    assert new_refsite is not refsite

    assert new_refsite.average_obstacle_height == refsite.average_obstacle_height
    assert new_refsite.vegetation_coverage == refsite.vegetation_coverage
    assert new_refsite.temp_measure_height == refsite.temp_measure_height
    assert new_refsite.wind_measure_height == refsite.wind_measure_height


def test_to_from_dict():
    """Test the VegetationPararameter to_dict and from_dict methods."""
    refsite = custom_refsite()
    refsite_dict = refsite.to_dict()
    new_refsite = ReferenceEPWSite.from_dict(refsite_dict)

    assert new_refsite.average_obstacle_height == refsite.average_obstacle_height
    assert new_refsite.vegetation_coverage == refsite.vegetation_coverage
    assert new_refsite.temp_measure_height == refsite.temp_measure_height
    assert new_refsite.wind_measure_height == refsite.wind_measure_height
