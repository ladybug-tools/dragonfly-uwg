# coding=utf-8
from dragonfly_uwg.terrain import Terrain

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D


def base_terrain():
    ter_geo = Face3D((Point3D(0, 0, 0), Point3D(30, 0, 0),
                      Point3D(30, 30, 0), Point3D(0, 30, 3)))
    terrain = Terrain([ter_geo])
    return terrain


def custom_terrain():
    ter_geo = Face3D((Point3D(0, 0, 0), Point3D(30, 0, 0),
                      Point3D(30, 30, 0), Point3D(0, 30, 3)))
    terrain = Terrain([ter_geo], 0.15, 0.75, 2, 2.0e6)
    return terrain
