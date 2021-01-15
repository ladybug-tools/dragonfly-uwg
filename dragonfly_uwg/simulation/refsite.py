# coding=utf-8
from __future__ import division

from honeybee.typing import float_in_range, float_positive


class ReferenceEPWSite(object):
    """Properties of the reference site where the input rural EPW was recorded.

    Args:
        average_obstacle_height: A number that represents the height in meters of
            objects that obstruct the view to the sky at the weather station site.
            This includes both trees and buildings. (Default: 0.1 m).
        vegetation_coverage: A number between 0 and 1 that represents the fraction
            of the reference EPW site that is covered in grass. (Default: 0.9).
        temp_measure_height: A number that represents the height in meters at which
            temperature is measured on the weather station. (Default: 10m, the
            standard measurement height for US DoE EPW files).
        wind_measure_height: A number that represents the height in meters at which
            wind speed is measured on the weather station. (Default: 10m, the
            standard measurement height for US DoE EPW files).
    """
    __slots__ = ('_average_obstacle_height', '_vegetation_coverage',
                 '_temp_measure_height', '_wind_measure_height')

    def __init__(self, average_obstacle_height=0.1, vegetation_coverage=0.9,
                 temp_measure_height=10, wind_measure_height=10):
        """Initialize ReferenceEPWSite parameters"""
        self.average_obstacle_height = average_obstacle_height
        self.vegetation_coverage = vegetation_coverage
        self.temp_measure_height = temp_measure_height
        self.wind_measure_height = wind_measure_height

    @classmethod
    def from_dict(cls, data):
        """Create a ReferenceEPWSite object from a dictionary

        Args:
            data: A dictionary representation of an ReferenceEPWSite object
                in the format below.

        .. code-block:: python

            {
            'type': 'ReferenceEPWSite',
            'average_obstacle_height': 10,  # float for obstacle height in meters
            'vegetation_coverage': 0.95,  # float for vegetation coverage between 0 and 1
            'temp_measure_height': 10,  # float for temp measurement height in meters
            'wind_measure_height: 15  # float for wind measurement height in meters
            }
        """
        ob_hgt = data['average_obstacle_height'] \
            if 'average_obstacle_height' in data else 0.1
        veg_cov = data['vegetation_coverage'] \
            if 'vegetation_coverage' in data else 0.9
        temp = data['temp_measure_height'] \
            if 'temp_measure_height' in data else 10
        wind = data['wind_measure_height'] \
            if 'wind_measure_height' in data else 10
        return cls(ob_hgt, veg_cov, temp, wind)

    @property
    def average_obstacle_height(self):
        """Get or set a number for the average obstacle height in meters."""
        return self._average_obstacle_height

    @average_obstacle_height.setter
    def average_obstacle_height(self, value):
        self._average_obstacle_height = float_positive(value, 'average_obstacle_height')

    @property
    def vegetation_coverage(self):
        """Get or set a fractional number for the vegetation coverage."""
        return self._vegetation_coverage

    @vegetation_coverage.setter
    def vegetation_coverage(self, value):
        self._vegetation_coverage = float_in_range(value, 0, 1, 'vegetation_coverage')

    @property
    def temp_measure_height(self):
        """Get or set a number for the temperature measurement height in meters."""
        return self._temp_measure_height

    @temp_measure_height.setter
    def temp_measure_height(self, value):
        self._temp_measure_height = float_positive(value, 'temp_measure_height')

    @property
    def wind_measure_height(self):
        """Get or set a number for the wind measurement height in meters."""
        return self._wind_measure_height

    @wind_measure_height.setter
    def wind_measure_height(self, value):
        self._wind_measure_height = float_positive(value, 'wind_measure_height')

    def to_dict(self):
        """Get ReferenceEPWSite dictionary."""
        return {
            'type': 'ReferenceEPWSite',
            'average_obstacle_height': self.average_obstacle_height,
            'vegetation_coverage': self.vegetation_coverage,
            'temp_measure_height': self.temp_measure_height,
            'wind_measure_height': self.wind_measure_height}

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        return ReferenceEPWSite(
            self._average_obstacle_height, self._vegetation_coverage,
            self._temp_measure_height, self._wind_measure_height)

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represent Dragonfly reference EPW site parameters."""
        return 'ReferenceEPWSite: [obstacle height: {} m] [veg coverage: {}]'.format(
                self._average_obstacle_height, self._vegetation_coverage)
