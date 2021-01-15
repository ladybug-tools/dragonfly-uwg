# coding=utf-8
from dragonfly_uwg.terrain import Terrain

from ladybug_geometry.geometry3d.face import Face3D

from tests.fixtures.terrain import base_terrain, custom_terrain


def test_terrain():
    """Test the existence of basic properties."""
    terrain = base_terrain()

    str(terrain)  # test the string representation
    assert len(terrain.geometry) == 1
    assert isinstance(terrain.geometry[0], Face3D)
    assert terrain.pavement_albedo == 0.1
    assert terrain.pavement_thickness == 0.5
    assert terrain.pavement_conductivity == 1.0
    assert terrain.pavement_heat_capacity == 1.6e6


def test_duplicate():
    """Test the duplicate method."""
    terrain = custom_terrain()
    new_terrain = terrain.duplicate()
    assert new_terrain is not terrain

    assert new_terrain.geometry[0] == terrain.geometry[0]
    assert new_terrain.pavement_albedo == terrain.pavement_albedo
    assert new_terrain.pavement_thickness == terrain.pavement_thickness
    assert new_terrain.pavement_conductivity == terrain.pavement_conductivity
    assert new_terrain.pavement_heat_capacity == terrain.pavement_heat_capacity


def test_to_from_dict():
    """Test the Terrain to_dict and from_dict methods."""
    terrain = custom_terrain()
    terrain_dict = terrain.to_dict()
    new_terrain = Terrain.from_dict(terrain_dict)

    assert new_terrain.geometry[0] == terrain.geometry[0]
    assert new_terrain.pavement_albedo == terrain.pavement_albedo
    assert new_terrain.pavement_thickness == terrain.pavement_thickness
    assert new_terrain.pavement_conductivity == terrain.pavement_conductivity
    assert new_terrain.pavement_heat_capacity == terrain.pavement_heat_capacity
    assert new_terrain.to_dict() == terrain_dict
