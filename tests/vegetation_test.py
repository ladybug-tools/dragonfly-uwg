# coding=utf-8
from dragonfly_uwg.simulation.vegetation import VegetationParameter

from honeybee.altnumber import autocalculate

from tests.fixtures.vegetation import default_vegetation, custom_vegetation


def test_vegetation():
    """Test the existence of basic properties."""
    vegetation = default_vegetation()

    str(vegetation)  # test the string representation
    assert vegetation.vegetation_albedo == 0.25
    assert vegetation.start_month == autocalculate
    assert vegetation.end_month == autocalculate
    assert vegetation.tree_latent_fraction == 0.7
    assert vegetation.grass_latent_fraction == 0.5


def test_duplicate():
    """Test the duplicate method."""
    vegetation = custom_vegetation()
    new_vegetation = vegetation.duplicate()
    assert new_vegetation is not vegetation

    assert new_vegetation.vegetation_albedo == vegetation.vegetation_albedo
    assert new_vegetation.start_month == vegetation.start_month
    assert new_vegetation.end_month == vegetation.end_month
    assert new_vegetation.tree_latent_fraction == vegetation.tree_latent_fraction
    assert new_vegetation.grass_latent_fraction == vegetation.grass_latent_fraction


def test_to_from_dict():
    """Test the VegetationPararameter to_dict and from_dict methods."""
    vegetation = custom_vegetation()
    vegetation_dict = vegetation.to_dict()
    new_vegetation = VegetationParameter.from_dict(vegetation_dict)

    assert new_vegetation.vegetation_albedo == vegetation.vegetation_albedo
    assert new_vegetation.start_month == vegetation.start_month
    assert new_vegetation.end_month == vegetation.end_month
    assert new_vegetation.tree_latent_fraction == vegetation.tree_latent_fraction
    assert new_vegetation.grass_latent_fraction == vegetation.grass_latent_fraction
    assert new_vegetation.to_dict() == vegetation_dict
