# coding=utf-8
from __future__ import division

from honeybee.typing import float_in_range, float_positive
from honeybee.altnumber import autocalculate


class TrafficParameter(object):
    """Object representing the traffic within an urban area.

    Note:
        [1] Sailor, David J. (2011). A review of methods for estimating anthropogenic
        heat and moisture emissions in the urban environment. Royal Meteorological
        Society, Volume 31, Issue 2, Pages 189-199. https://doi.org/10.1002/joc.2106

    Args:
        watts_per_area: A number representing the maximum sensible anthropogenic heat
            flux of the urban area in watts per square meter. This is specifically the
            heat that DOES NOT originate from buildings and mostly includes heat
            from automobiles, street lighting, and human metabolism. If autocalculate,
            it will be estimated frm the average building story count of the model
            hosting the traffic parameters (Default: autocalculate). Values
            for different cities can be found in (Sailor, 2011)[1]. Typical
            values include:

            * 20 W/m2 = A typical downtown area
            * 10 W/m2 = A commercial area in Singapore
            * 8 W/m2 = A typical mixed use part of Toulouse, France
            * 4 W/m2 = A residential area in Singapore

        weekday_schedule: A list of 24 fractional values that will be
            multiplied by the watts_per_area to produce hourly values for
            heat on the weekday of the simulation. (Default: a typical schedule
            for a commercial area).
        saturday_schedule: A list of 24 fractional values that will be
            multiplied by the watts_per_area to produce hourly values for
            heat on the Saturday of the simulation. (Default: a typical schedule
            for a commercial area).
        sunday_schedule: A list of 24 fractional values that will be
            multiplied by the watts_per_area to produce hourly values for
            heat on the Sunday of the simulation. (Default: a typical schedule
            for a commercial area).
    """
    __slots__ = ('_watts_per_area', '_weekday_schedule', '_saturday_schedule',
                 '_sunday_schedule')

    WEEKDAY_DEFAULT = \
        (0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.7, 0.9, 0.9, 0.6, 0.6, 0.6,
         0.6, 0.6, 0.7, 0.8, 0.9, 0.9, 0.8, 0.8, 0.7, 0.3, 0.2, 0.2)
    SATURDAY_DEFAULT = \
        (0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
         0.5, 0.5, 0.6, 0.7, 0.7, 0.7, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2)
    SUNDAY_DEFAULT = \
        (0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
         0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2)

    def __init__(self, watts_per_area=autocalculate, weekday_schedule=None,
                 saturday_schedule=None, sunday_schedule=None):
        """Initialize dragonfly traffic parameters"""
        self.watts_per_area = watts_per_area
        self.weekday_schedule = weekday_schedule
        self.saturday_schedule = saturday_schedule
        self.sunday_schedule = sunday_schedule

    @classmethod
    def from_dict(cls, data):
        """Initialize an TrafficParameter from a dictionary.

        Args:
            data: A dictionary representation of an TrafficParameter object
                in the format below.

        .. code-block:: python

            {
            "type": 'TrafficParameter',
            "watts_per_area": 10,  # number for heat in W/m2
            "weekday_schedule": [],  # list of 24 fractional values for a schedule
            "saturday_schedule": [],  # list of 24 fractional values for a schedule
            "sunday_schedule": []  # list of 24 fractional values for a schedule
            }
        """
        watts = autocalculate if 'watts_per_area' not in data or \
            data['watts_per_area'] == autocalculate.to_dict() else data['watts_per_area']
        weekday = data['weekday_schedule'] if 'weekday_schedule' in data else None
        saturday = data['saturday_schedule'] if 'saturday_schedule' in data else None
        sunday = data['sunday_schedule'] if 'sunday_schedule' in data else None
        return cls(watts, weekday, saturday, sunday)

    @property
    def watts_per_area(self):
        """Get or set a number for the max sensible heat flux of the traffic."""
        return self._watts_per_area if self._watts_per_area is not None \
            else autocalculate

    @watts_per_area.setter
    def watts_per_area(self, value):
        if value == autocalculate:
            self._watts_per_area = None
        else:
            self._watts_per_area = float_positive(value, 'traffic watts per area')

    @property
    def weekday_schedule(self):
        """Get or set the Weekday traffic schedule as a list of 24 fractional values."""
        return self._weekday_schedule if self._weekday_schedule is not None \
            else self.WEEKDAY_DEFAULT

    @weekday_schedule.setter
    def weekday_schedule(self, value):
        self._weekday_schedule = self._check_schedule(value) \
            if value is not None else None

    @property
    def saturday_schedule(self):
        """Get or set the Saturday traffic schedule as a list of 24 fractional values."""
        return self._saturday_schedule if self._saturday_schedule is not None \
            else self.SATURDAY_DEFAULT

    @saturday_schedule.setter
    def saturday_schedule(self, value):
        self._saturday_schedule = self._check_schedule(value) \
            if value is not None else None

    @property
    def sunday_schedule(self):
        """Get or set the Sunday traffic schedule as a list of 24 fractional values."""
        return self._sunday_schedule if self._sunday_schedule is not None \
            else self.SUNDAY_DEFAULT

    @sunday_schedule.setter
    def sunday_schedule(self, value):
        self._sunday_schedule = self._check_schedule(value) \
            if value is not None else None

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def to_dict(self):
        """Get TrafficParameter as a dictionary."""
        base = {'type': 'TrafficParameter'}
        if self._watts_per_area is not None:
            base['watts_per_area'] = self._watts_per_area
        if self._weekday_schedule is not None:
            base['weekday_schedule'] = self._weekday_schedule
        if self._saturday_schedule is not None:
            base['saturday_schedule'] = self._saturday_schedule
        if self._sunday_schedule is not None:
            base['sunday_schedule'] = self._sunday_schedule
        return base

    def _check_schedule(self, schedule):
        if len(schedule) == 24:
            return tuple(float_in_range(x, 0, 1, 'schedule value') for x in schedule)
        else:
            raise ValueError(
                'Traffic schedules must be lists of 24 values. Current schedule '
                'has length ({})'.format(len(schedule)))

    def __copy__(self):
        new_obj = TrafficParameter()
        new_obj._watts_per_area = self._watts_per_area
        new_obj._weekday_schedule = self._weekday_schedule
        new_obj._saturday_schedule = self._saturday_schedule
        new_obj._sunday_schedule = self._sunday_schedule
        return new_obj

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represent Dragonfly traffic parameters."""
        return 'TrafficParameter: [{} W/m2]'.format(self.watts_per_area)
