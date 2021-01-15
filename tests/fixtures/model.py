# coding=utf-8
from dragonfly_uwg.terrain import Terrain

from dragonfly.model import Model
from dragonfly.building import Building
from dragonfly.story import Story
from dragonfly.room2d import Room2D
from dragonfly.context import ContextShade
from dragonfly.windowparameter import SimpleWindowRatio

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D


def two_buildings():
    pts_1 = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(20, 0, 3), Point3D(20, 10, 3),
             Point3D(10, 10, 3))
    pts_3 = (Point3D(0, 20, 3), Point3D(20, 20, 3), Point3D(20, 30, 3),
             Point3D(0, 30, 3))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    room2d_3 = Room2D('Office3', Face3D(pts_3), 3)
    story_big = Story('OfficeFloorBig', [room2d_3])
    story = Story('OfficeFloor', [room2d_1, room2d_2])
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.3))
    story.multiplier = 3
    building = Building('OfficeBuilding', [story])
    building.separate_top_bottom_floors()
    story_big.set_outdoor_window_parameters(SimpleWindowRatio(0.6))
    story_big.multiplier = 4
    building_big = Building('OfficeBuildingBig', [story_big])
    building_big.separate_top_bottom_floors()

    tree_canopy_geo1 = Face3D.from_regular_polygon(6, 6, Plane(o=Point3D(5, -10, 6)))
    tree_canopy_geo2 = Face3D.from_regular_polygon(6, 2, Plane(o=Point3D(-5, -10, 3)))
    tree_canopy = ContextShade('TreeCanopy', [tree_canopy_geo1, tree_canopy_geo2])

    model = Model('NewDevelopment', [building, building_big], [tree_canopy])
    return model


def two_buildings_with_terrain():
    pts_1 = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(20, 0, 3), Point3D(20, 10, 3),
             Point3D(10, 10, 3))
    pts_3 = (Point3D(0, 20, 3), Point3D(20, 20, 3), Point3D(20, 30, 3),
             Point3D(0, 30, 3))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    room2d_3 = Room2D('Office3', Face3D(pts_3), 3)
    story_big = Story('OfficeFloorBig', [room2d_3])
    story = Story('OfficeFloor', [room2d_1, room2d_2])
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.3))
    story.multiplier = 3
    building = Building('OfficeBuilding', [story])
    building.separate_top_bottom_floors()
    story_big.set_outdoor_window_parameters(SimpleWindowRatio(0.6))
    story_big.multiplier = 4
    building_big = Building('OfficeBuildingBig', [story_big])
    building_big.separate_top_bottom_floors()

    tree_canopy_geo1 = Face3D.from_regular_polygon(6, 6, Plane(o=Point3D(5, -10, 6)))
    tree_canopy_geo2 = Face3D.from_regular_polygon(6, 2, Plane(o=Point3D(-5, -10, 3)))
    tree_canopy = ContextShade('TreeCanopy', [tree_canopy_geo1, tree_canopy_geo2])

    model = Model('NewDevelopment', [building, building_big], [tree_canopy])

    ter_geo = Face3D((Point3D(0, 0, 0), Point3D(30, 0, 0),
                      Point3D(30, 30, 0), Point3D(0, 30, 3)))
    terrain = Terrain([ter_geo])
    model.properties.uwg.terrain = terrain
    model.properties.uwg.traffic.watts_per_area = 7
    model.properties.uwg.tree_coverage_fraction = 0.25
    model.properties.uwg.grass_coverage_fraction = 0.4

    return model
