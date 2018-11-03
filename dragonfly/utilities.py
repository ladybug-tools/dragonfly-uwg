# coding=utf-8
"""A collection of auxiliary funtions for checking inputs."""


def in_range(self, val, low, high, param_name='parameter'):
    if val <= high and val >= low:
        return val
    else:
        raise ValueError(
            "{} must be between {} and {}. Current value is {}".format(
                param_name, str(low), str(high), str(val)))


def length_match(list1, list2, list1_name='list1', list2_name='list2'):
    if len(list1) == len(list2):
        return True
    else:
        raise ValueError(
            "Length of {} : {} does not match the length of {} : {}"
            .format(list1_name,
                    str(len(list1)),
                    list2_name,
                    str(len(list1)))
                    )


def fixRange(self, val, low, high):
    if val > high:
        return high
    elif val < low:
        return low
    else:
        return float(val)
