# coding=utf-8
from dragonfly_uwg.simulation.refsite import ReferenceEPWSite


def default_refsite():
    return ReferenceEPWSite()


def custom_refsite():
    return ReferenceEPWSite(1, 0.95, 15, 15)
