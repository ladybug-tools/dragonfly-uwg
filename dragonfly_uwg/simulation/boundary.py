# coding=utf-8
from __future__ import division

from honeybee.typing import float_positive


class BoundaryLayerParameter(object):
    """Properties of the urban boundary layer.

    Args:
        day_boundary_layer_height: A number that represents the height
            in meters of the urban boundary layer during the daytime.
            This is the height to which the urban meteorological conditions
            are stable and representative of the overall urban area.
            Typically, this boundary layer height increases with the
            height of the buildings. (Default: 1000 meters).
        night_boundary_layer_height: A number that represents the height
            in meters of the urban boundary layer during the nighttime.
            This is the height to which the urban meteorological
            conditions are stable and representative of the overall
            urban area. Typically, this boundary layer height increases with
            the height of the buildings. (Default: 80 meters).
        inversion_height: A number that represents the height in meters at which
            the vertical profile of potential temperature becomes stable.
            Can be determined by flying helium balloons equipped
            with temperature sensors and recording the air temperatures
            at different heights. (Default: 150 meters).
        circulation_coefficient: A number representing the circulation
            coefficient. (Default: 1.2, per Bueno (2012)).
        exchange_coefficient: A number representing the exchange
            coefficient. (Default: 1.0, per Bueno (2014)).
    """

    __slots__ = ('_day_boundary_layer_height', '_night_boundary_layer_height',
                 '_inversion_height', '_circulation_coefficient',
                 '_exchange_coefficient')

    def __init__(self, day_boundary_layer_height=1000, night_boundary_layer_height=80,
                 inversion_height=150,
                 circulation_coefficient=1.2, exchange_coefficient=1.0):
        """Initialize Boundary Layer parameters"""
        self.day_boundary_layer_height = day_boundary_layer_height
        self.night_boundary_layer_height = night_boundary_layer_height
        self.inversion_height = inversion_height
        self.circulation_coefficient = circulation_coefficient
        self.exchange_coefficient = exchange_coefficient

    @classmethod
    def from_dict(cls, data):
        """Create a BoundaryLayerParameter object from a dictionary

        Args:
            data: A dictionary representation of an BoundaryLayerParameter object
                in the format below.

        .. code-block:: python

            {
            'type': 'BoundaryLayerParameter',
            'day_boundary_layer_height': 1000,  # float for height in meters
            'night_boundary_layer_height': 80,  # float for height in meters
            'inversion_height': 150,  # float for inversion layer height
            'circulation_coefficient': 1.2,  # float for circulation coefficient
            'exchange_coefficient': 1.0  # float for exchange coefficient
            }
        """
        day = data['day_boundary_layer_height'] \
            if 'day_boundary_layer_height' in data else 1000
        night = data['night_boundary_layer_height'] \
            if 'night_boundary_layer_height' in data else 80
        inv = data['inversion_height'] if 'inversion_height' in data else 150
        circ = data['circulation_coefficient'] \
            if 'circulation_coefficient' in data else 1.2
        exch = data['exchange_coefficient'] \
            if 'exchange_coefficient' in data else 1.0
        return cls(day, night, inv, circ, exch)

    @property
    def day_boundary_layer_height(self):
        """Get or set a number for the daytime boundary layer height in meters."""
        return self._day_boundary_layer_height

    @day_boundary_layer_height.setter
    def day_boundary_layer_height(self, value):
        self._day_boundary_layer_height = \
            float_positive(value, 'day_boundary_layer_height')

    @property
    def night_boundary_layer_height(self):
        """Get or set a number for the nighttime boundary layer height i meters."""
        return self._night_boundary_layer_height

    @night_boundary_layer_height.setter
    def night_boundary_layer_height(self, value):
        self._night_boundary_layer_height = \
            float_positive(value, 'night_boundary_layer_height')

    @property
    def inversion_height(self):
        """Get or set a number for the inversion height in meters."""
        return self._inversion_height

    @inversion_height.setter
    def inversion_height(self, value):
        self._inversion_height = float_positive(value, 'inversion_height')

    @property
    def circulation_coefficient(self):
        """Get or set a number for the circulation coefficient."""
        return self._circulation_coefficient

    @circulation_coefficient.setter
    def circulation_coefficient(self, value):
        self._circulation_coefficient = float_positive(value, 'circulation_coefficient')

    @property
    def exchange_coefficient(self):
        """Get or set the exchange coefficient."""
        return self._exchange_coefficient

    @exchange_coefficient.setter
    def exchange_coefficient(self, value):
        self._exchange_coefficient = float_positive(value, 'exchange_coefficient')

    def to_dict(self):
        """Get BoundaryLayerParameter dictionary."""
        return {
            'type': 'BoundaryLayerParameter',
            'day_boundary_layer_height': self.day_boundary_layer_height,
            'night_boundary_layer_height': self.night_boundary_layer_height,
            'inversion_height': self.inversion_height,
            'circulation_coefficient': self.circulation_coefficient,
            'exchange_coefficient': self.exchange_coefficient}

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        return BoundaryLayerParameter(
            self._day_boundary_layer_height, self._night_boundary_layer_height,
            self._inversion_height,
            self._circulation_coefficient, self._exchange_coefficient)

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represent Dragonfly boundary layer parameters."""
        return 'BoundaryLayerParameter: [boundary (day | night): {} m | {} m] ' \
            '[inversion: {} m]'.format(
                self.day_boundary_layer_height, self.night_boundary_layer_height,
                self.inversion_height)
