# coding=utf-8
from dragonfly_uwg.traffic import TrafficParameter


def default_traffic():
    return TrafficParameter()


def custom_traffic():
    custom_sch = \
        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.9, 0.6, 0.6, 0.6,
         0.6, 0.6, 0.7, 0.8, 0.9, 0.9, 0.8, 0.8, 0.0, 0.0, 0.0, 0.0)
    return TrafficParameter(8, custom_sch, custom_sch, custom_sch)
