# coding=utf-8
"""A collection of auxiliary funtions for checking inputs."""


def in_range(val, low, high, param_name='parameter'):
    if val <= high and val >= low:
        return val
    else:
        raise ValueError(
            "{} must be between {} and {}. Current value is {}".format(
                param_name, str(low), str(high), str(val)))


def fixRange(val, low, high):
    if val > high:
        return high
    elif val < low:
        return low
    else:
        return float(val)
