# coding=utf-8
from dragonfly_uwg.traffic import TrafficPararameter


def default_traffic():
    return TrafficPararameter()


def custom_traffic():
    custom_sch = \
        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.9, 0.6, 0.6, 0.6,
         0.6, 0.6, 0.7, 0.8, 0.9, 0.9, 0.8, 0.8, 0.0, 0.0, 0.0, 0.0)
    return TrafficPararameter(8, custom_sch, custom_sch, custom_sch)
