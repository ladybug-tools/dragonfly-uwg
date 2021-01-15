# coding=utf-8
import pytest
import math

from dragonfly_uwg.properties.model import ModelUWGProperties
from dragonfly_uwg.terrain import Terrain
from dragonfly_uwg.traffic import TrafficPararameter

from dragonfly.model import Model
from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
from ladybug_geometry.geometry3d.plane import Plane

from tests.fixtures.model import two_buildings, two_buildings_with_terrain


def test_uwg_properties():
    """Test the existence of the Model UWG properties."""
    model = two_buildings()

    assert hasattr(model.properties, 'uwg')
    assert isinstance(model.properties.uwg, ModelUWGProperties)
    str(model.properties.uwg)  # test the string representation
    assert isinstance(model.properties.host, Model)
    assert isinstance(model.properties.uwg.terrain, Terrain)
    assert isinstance(model.properties.uwg.traffic, TrafficPararameter)
    assert model.properties.uwg.tree_coverage_fraction == 0
    assert model.properties.uwg.grass_coverage_fraction == 0


def test_duplicate():
    """Test the duplicate method."""
    model = two_buildings_with_terrain()
    new_model = model.duplicate()
    assert new_model is not model

    assert new_model.properties.uwg.terrain.geometry[0] == \
        model.properties.uwg.terrain.geometry[0]
    assert new_model.properties.uwg.traffic.watts_per_area == 7
    assert new_model.properties.uwg.tree_coverage_fraction == 0.25
    assert new_model.properties.uwg.grass_coverage_fraction == 0.4


def test_move():
    """Test the move method."""
    model = two_buildings_with_terrain()
    terrain_geo = model.properties.uwg.terrain.geometry[0]

    move_vec = Vector3D(1, 1, 1)
    model.move(move_vec)
    assert model.properties.uwg.terrain.geometry[0] == terrain_geo.move(move_vec)


def test_rotate_xy():
    """Test the rotate_xy method."""
    model = two_buildings_with_terrain()
    terrain_geo = model.properties.uwg.terrain.geometry[0]

    angle, origin = 90, Point3D(10, 10, 0)
    model.rotate_xy(angle, origin)
    assert model.properties.uwg.terrain.geometry[0] == \
        terrain_geo.rotate_xy(math.radians(angle), origin)


def test_reflect():
    """Test the reflect method."""
    model = two_buildings_with_terrain()
    terrain_geo = model.properties.uwg.terrain.geometry[0]

    ref_plane = Plane(n=Vector3D(1, 0, 0))
    model.reflect(ref_plane)
    assert model.properties.uwg.terrain.geometry[0] == \
        terrain_geo.reflect(ref_plane.n, ref_plane.o)


def test_scale():
    """Test the scale method."""
    model = two_buildings_with_terrain()
    terrain_geo = model.properties.uwg.terrain.geometry[0]

    scale_fac = 2
    model.scale(scale_fac)
    assert model.properties.uwg.terrain.geometry[0] == terrain_geo.scale(scale_fac)


def test_to_from_dict():
    """Test the Model to_dict and from_dict methods."""
    model = two_buildings_with_terrain()

    model_dict = model.to_dict()

    assert 'uwg' in model_dict['properties']
    assert 'terrain' in model_dict['properties']['uwg']
    assert 'traffic' in model_dict['properties']['uwg']
    assert 'tree_coverage_fraction' in model_dict['properties']['uwg']
    assert 'grass_coverage_fraction' in model_dict['properties']['uwg']

    new_model = Model.from_dict(model_dict)

    assert new_model.properties.uwg.terrain.geometry[0] == \
        model.properties.uwg.terrain.geometry[0]
    assert new_model.properties.uwg.traffic.watts_per_area == 7
    assert new_model.properties.uwg.tree_coverage_fraction == 0.25
    assert new_model.properties.uwg.grass_coverage_fraction == 0.4


def test_model_to_uwg_dict():
    """Test the existence of the Model.to.uwg."""
    model = two_buildings()

    epw_path = './tests/epw/boston.epw'
    uwg_dict = model.to.uwg(model, epw_path)
    print(uwg_dict)
