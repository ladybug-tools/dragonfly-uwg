# coding=utf-8
"""UWG Simulation Run Period."""
from __future__ import division

from ladybug.analysisperiod import AnalysisPeriod
from ladybug.dt import Date


class UWGRunPeriod(object):
    """UWG Simulation Run Period.

    Args:
        start_date: A ladybug Date object for the start of the simulation.
            Must be before the end date and have a leap_year property matching the
            end_date. (Default: 1 Jan).
        end_date: A ladybug Date object for the end of the simulation.
            Must be after the start date and have a leap_year property matching the
            start_date. (Default: 31 Dec).

    Properties:
        * start_date
        * end_date
        * day_count
    """
    __slots__ = ('_start_date', '_end_date')

    def __init__(self, start_date=Date(1, 1), end_date=Date(12, 31)):
        """Initialize UWGRunPeriod."""
        # process the dates
        if start_date is not None:
            self._check_date(start_date, 'start_date')
            self._start_date = start_date
        else:
            self._start_date = Date(1, 1)
        self.end_date = end_date

    @property
    def start_date(self):
        """Get or set a ladybug Date object for the start of the simulation period."""
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if value is not None:
            self._check_date(value, 'start_date')
            self._start_date = value
        else:
            self._start_date = Date(1, 1)
        self._check_start_before_end()

    @property
    def end_date(self):
        """Get or set a ladybug Date object for the end of the simulation period."""
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        if value is not None:
            self._check_date(value, 'end_date')
            self._end_date = value
        else:
            self._end_date = Date(12, 31)
        self._check_start_before_end()

    @property
    def day_count(self):
        """Get an integer for the number of days in the run period."""
        return int(self.end_date.doy - self.start_date.doy + 1)

    @classmethod
    def from_analysis_period(cls, analysis_period=AnalysisPeriod(1, 1, 0, 12, 31, 23)):
        """Initialize a UWGRunPeriod object from a ladybug AnalysisPeriod.

        Args:
            analysis_period: A ladybug AnalysisPeriod object that has the start
                and end dates for daylight savings time.
        """
        assert isinstance(analysis_period, AnalysisPeriod), 'Expected AnalysisPeriod ' \
            'for UWGRunPeriod.from_analysis_period. Got {}.'.format(
                type(analysis_period))
        st_date = Date(analysis_period.st_month, analysis_period.st_day,
                       analysis_period.is_leap_year)
        end_date = Date(analysis_period.end_month, analysis_period.end_day,
                        analysis_period.is_leap_year)
        return cls(st_date, end_date)

    @classmethod
    def from_dict(cls, data):
        """Create a UWGRunPeriod object from a dictionary.

        Args:
            data: A UWGRunPeriod dictionary in following the format below.

        .. code-block:: python

            {
            "type": "UWGRunPeriod",
            "start_date": [3, 12],
            "end_date": [11, 5]
            }
        """
        assert data['type'] == 'UWGRunPeriod', \
            'Expected UWGRunPeriod dictionary. Got {}.'.format(data['type'])
        start_date = Date.from_array(data['start_date']) if 'start_date' in data and \
            data['start_date'] is not None else Date(1, 1)
        end_date = Date.from_array(data['end_date']) if 'end_date' in data and \
            data['end_date'] is not None else Date(12, 31)
        return cls(start_date, end_date)

    def to_dict(self):
        """UWGRunPeriod dictionary representation."""
        return {
            'type': 'UWGRunPeriod',
            'start_date': self.start_date.to_array(),
            'end_date': self.end_date.to_array()
        }

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def _check_start_before_end(self):
        """Check that the start_date is before the end_date."""
        assert self.start_date.leap_year is self.end_date.leap_year, \
            'UWGRunPeriod start_date.leap_year must match the end_date.leap_year'
        assert self._start_date <= self._end_date, 'UWGRunPeriod start_date must ' \
            'be before end_date. {} is after {}.'.format(self.start_date, self.end_date)

    @staticmethod
    def _check_date(date, date_name='date'):
        assert isinstance(date, Date), 'Expected ladybug Date for ' \
            'UWGRunPeriod {}. Got {}.'.format(date_name, type(date))

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __copy__(self):
        return UWGRunPeriod(self.start_date, self.end_date)

    def __repr__(self):
        return 'UWGRunPeriod: [{} - {}]'.format(self.start_date, self.end_date)
