# coding=utf-8


class Utilities(object):
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

    def checkSchedule(self, schedule):
        if len(schedule) == 24:
            return [self.in_range(x, 0, 1, 'schedule value') for x in schedule]
        else:
            raise Exception(
                "Current schedule has length " + str(len(schedule)) +
                ". Daily schedules must be lists of 24 values."
            )

    def fixRange(self, val, low, high):
        if val > high:
            return high
        elif val < low:
            return low
        else:
            return float(val)
