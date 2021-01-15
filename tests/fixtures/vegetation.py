# coding=utf-8
from dragonfly_uwg.simulation.vegetation import VegetationParameter


def default_vegetation():
    return VegetationParameter()


def custom_vegetation():
    return VegetationParameter(0.4, 3, 11, 0.8, 0.6)
