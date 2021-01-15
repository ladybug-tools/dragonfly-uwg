# coding=utf-8
from dragonfly.building import Building
from dragonfly.story import Story
from dragonfly.room2d import Room2D
from dragonfly.windowparameter import SimpleWindowRatio

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D


def default_building():
    pts_1 = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(20, 0, 3), Point3D(20, 10, 3),
             Point3D(10, 10, 3))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    story = Story('OfficeFloor', [room2d_1, room2d_2])
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.3))
    story.multiplier = 3
    building = Building('OfficeBuilding', [story])
    building.separate_top_bottom_floors()
    return building


def custom_building():
    pts_1 = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    pts_2 = (Point3D(10, 0, 3), Point3D(20, 0, 3), Point3D(20, 10, 3),
             Point3D(10, 10, 3))
    room2d_1 = Room2D('Office1', Face3D(pts_1), 3)
    room2d_2 = Room2D('Office2', Face3D(pts_2), 3)
    story = Story('OfficeFloor', [room2d_1, room2d_2])
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.3))
    story.multiplier = 3
    building = Building('OfficeBuilding', [story])
    building.separate_top_bottom_floors()

    building.properties.uwg.program == 'MidriseApartment'
    building.properties.uwg.vintage == 'Pre1980'
    building.properties.uwg.fract_heat_to_canyon == 1.0
    building.properties.uwg.shgc == 0.6
    building.properties.uwg.wall_albedo == 0.3
    building.properties.uwg.roof_albedo == 0.5
    building.properties.uwg.roof_veg_fraction == 0.3

    return building
