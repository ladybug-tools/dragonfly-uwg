# coding=utf-8
from dragonfly_uwg.simulation.boundary import BoundaryLayerParameter
from dragonfly_uwg.simulation.refsite import ReferenceEPWSite
from dragonfly_uwg.simulation.vegetation import VegetationParameter
from dragonfly_uwg.simulation.runperiod import UWGRunPeriod
from dragonfly_uwg.simulation.parameter import UWGSimulationParameter


def default_sim_par():
    return UWGSimulationParameter()


def custom_sim_par():
    veg = VegetationParameter(0.4, 3, 11, 0.8, 0.6)
    site = ReferenceEPWSite(1, 0.95, 15, 15)
    boundary = BoundaryLayerParameter(800, 200, 250, 1.5, 1.3)
    return UWGSimulationParameter('5A', UWGRunPeriod(), 6, veg, site, boundary)
