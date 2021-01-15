# coding=utf-8
from dragonfly_uwg.simulation.boundary import BoundaryLayerParameter


def default_boundary():
    return BoundaryLayerParameter()


def custom_boundary():
    return BoundaryLayerParameter(800, 200, 250, 1.5, 1.3)
