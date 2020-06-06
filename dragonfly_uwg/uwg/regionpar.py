# coding=utf-8
from __future__ import division

from ..dfobject import DFParameter
from ..utilities import in_range


class RefEPWSitePar(DFParameter):
    """Represents properties of the reference site where the original EPW was recorded.

    Properties:
        average_obstacle_height: A number that represents the height in
            meters of objects that obstruct the view to the sky at the
            weather station site.  This includes both trees and buildings.
            The default is set to 0.1 meters.
        vegetation_coverage: A number between 0 and 1 that represents
            that fraction of the reference EPW site that is covered in grass.
            If nothing is input here, a defailt of 0.9 will be used.
        temp_measure_height: A number that represents the height in meters
            at which temperature is measured on the weather station.
            The default is set to 10 meters as this is the standard
            measurement height for US Department of Energy EPW files.
        wind_measure_height: A number that represents the height in meters
            at which wind speed is measured on the weather station.
            The default is set to 10 meters as this is the standard
            measurement height for US Department of Energy EPW files.
    """

    def __init__(self, average_obstacle_height=None, vegetation_coverage=None,
                 temp_measure_height=None, wind_measure_height=None):
        """Initialize RefEPWSitePar parameters"""
        self.average_obstacle_height = average_obstacle_height
        self.vegetation_coverage = vegetation_coverage
        self.temp_measure_height = temp_measure_height
        self.wind_measure_height = wind_measure_height

    @classmethod
    def from_json(cls, data):
        """Create a reference epw parameter object from a dictionary
        Args:
            data: {
                average_obstacle_height: float
                vegetation_coverage: float between 0 and 1
                temp_measure_height: float between 0 and 1
                wind_measure_height: float
            }
        """

        required_keys = ()
        nullable_keys = ("average_obstacle_height", "vegetation_coverage",
                         "temp_measure_height", "wind_measure_height")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(average_obstacle_height=data["average_obstacle_height"],
                   vegetation_coverage=data["vegetation_coverage"],
                   temp_measure_height=data["temp_measure_height"],
                   wind_measure_height=data["wind_measure_height"])

    @property
    def average_obstacle_height(self):
        """Get or set the average obstacle height."""
        return self._average_obstacle_height

    @average_obstacle_height.setter
    def average_obstacle_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'average_obstacle_height must be a number got {}'.format(type(h))
            assert (h >= 0), "average_obstacle_height must be greater than 0"
            self._average_obstacle_height = h
        else:
            self._average_obstacle_height = 0.1

    @property
    def vegetation_coverage(self):
        """Get or set the vegetation coverage."""
        return self._vegetation_coverage

    @vegetation_coverage.setter
    def vegetation_coverage(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), \
                'vegetation_coverage must be a number got {}'.format(type(a))
            self._vegetation_coverage = in_range(a, 0, 1, 'vegetation_coverage')
        else:
            self._vegetation_coverage = 0.9

    @property
    def temp_measure_height(self):
        """Get or set the temperature measurement height."""
        return self._temp_measure_height

    @temp_measure_height.setter
    def temp_measure_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'temp_measure_height must be a number got {}'.format(type(h))
            assert (h >= 0), "temp_measure_height must be greater than 0"
            self._temp_measure_height = h
        else:
            self._temp_measure_height = 10

    @property
    def wind_measure_height(self):
        """Get or set the wind measurement height."""
        return self._wind_measure_height

    @wind_measure_height.setter
    def wind_measure_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'wind_measure_height must be a number got {}'.format(type(h))
            assert (h >= 0), "wind_measure_height must be greater than 0"
            self._wind_measure_height = h
        else:
            self._wind_measure_height = 10

    @property
    def isRefEPWSitePar(self):
        """Return True for isRefEPWSitePar."""
        return True

    def to_json(self):
        """Create a reference epw parameter dictionary
        Results:
            {
                average_obstacle_height: float
                vegetation_coverage: float between 0 and 1
                temp_measure_height: float between 0 and 1
                wind_measure_height: float
            }
        """
        return {
            "average_obstacle_height": self.average_obstacle_height,
            "vegetation_coverage": self.vegetation_coverage,
            "temp_measure_height": self.temp_measure_height,
            "wind_measure_height": self.wind_measure_height
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly reference EPW site parameters."""
        return 'Reference EPW Site Parameters:' \
            '\n  Obstacle Height: {} m' \
            '\n  Vegetation Coverage: {}' \
            '\n  Measurement Height (Temp | Wind): {} m | {} m'.format(
                self._average_obstacle_height, self._vegetation_coverage,
                self._temp_measure_height, self._wind_measure_height
            )


class BoundaryLayerPar(DFParameter):
    """Represents the properties of the urban boundary layer.

    Properties:
        day_boundary_layer_height: A number that represents the height
            in meters of the urban boundary layer during the daytime.
            This is the height to which the urban meterorological conditions
            are stable and representative of the overall urban area.
            Typically, this boundary layer height increases with the
            height of the buildings.  The default is set to 1000 meters.
        night_boundary_layer_height: A number that represents the height
            in meters of the urban boundary layer during the nighttime.
            This is the height to which the urban meterorological
            conditions are stable and representative of the overall
            urban area. Typically, this boundary layer height increases with
            the height of the buildings.  The default is set to 80 meters.
        inversion_height: A number that represents the height at which
            the vertical profile of potential temperature becomes stable.
            It is the height at which the profile of air temperature becomes
            stable. Can be determined by flying helium balloons equipped
            with temperature sensors and recording the air temperatures
            at different heights.  The default is set to 150 meters.
        circulation_coefficient: A number representing the circulation coefficient.
            The default is 1.2 per Bueno, Bruno (2012).
        exchange_coefficient: A number representing the exchange coefficient.
            The default is 1.0 per Bueno, Bruno (2014).
    """

    def __init__(self, day_boundary_layer_height=None,
                 night_boundary_layer_height=None,
                 inversion_height=None,
                 circulation_coefficient=None, exchange_coefficient=None):
        """Initialize Boundary Layer parameters"""
        self.day_boundary_layer_height = day_boundary_layer_height
        self.night_boundary_layer_height = night_boundary_layer_height
        self.inversion_height = inversion_height
        self.circulation_coefficient = circulation_coefficient
        self.exchange_coefficient = exchange_coefficient

    @classmethod
    def from_json(cls, data):
        """Create a boundary layer parameter object from a dictionary
        Args:
            data: {
                day_boundary_layer_height: float positive
                night_boundary_layer_height: float positive
                inversion_height: float positive
                circulation_coefficient: float positive
                exchange_coefficient: float positive
            }
        """

        required_keys = ()
        nullable_keys = ("day_boundary_layer_height", "night_boundary_layer_height",
                         "inversion_height", "circulation_coefficient",
                         "exchange_coefficient")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(day_boundary_layer_height=data["day_boundary_layer_height"],
                   night_boundary_layer_height=data["night_boundary_layer_height"],
                   inversion_height=data["inversion_height"],
                   circulation_coefficient=data["circulation_coefficient"],
                   exchange_coefficient=data["exchange_coefficient"])

    @property
    def day_boundary_layer_height(self):
        """Get or set the daytime boundary layer height."""
        return self._day_boundary_layer_height

    @day_boundary_layer_height.setter
    def day_boundary_layer_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'day_boundary_layer_height must be a number got {}'.format(type(h))
            assert (h >= 0), "day_boundary_layer_height must be greater than 0"
            self._day_boundary_layer_height = h
        else:
            self._day_boundary_layer_height = 1000

    @property
    def night_boundary_layer_height(self):
        """Get or set the nighttime boundary layer height."""
        return self._night_boundary_layer_height

    @night_boundary_layer_height.setter
    def night_boundary_layer_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'night_boundary_layer_height must be a number got {}'.format(type(h))
            assert (h >= 0), "night_boundary_layer_height must be greater than 0"
            self._night_boundary_layer_height = h
        else:
            self._night_boundary_layer_height = 80

    @property
    def inversion_height(self):
        """Get or set the inversion height."""
        return self._inversion_height

    @inversion_height.setter
    def inversion_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'inversion_height must be a number got {}'.format(type(h))
            assert (h >= 0), "inversion_height must be greater than 0"
            self._inversion_height = h
        else:
            self._inversion_height = 150

    @property
    def circulation_coefficient(self):
        """Get or set the circulation coefficient."""
        return self._circulation_coefficient

    @circulation_coefficient.setter
    def circulation_coefficient(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'circulation_coefficient must be a number got {}'.format(type(h))
            self._circulation_coefficient = h
        else:
            self._circulation_coefficient = 1.2

    @property
    def exchange_coefficient(self):
        """Get or set the exchange coefficient."""
        return self._exchange_coefficient

    @exchange_coefficient.setter
    def exchange_coefficient(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), \
                'exchange_coefficient must be a number got {}'.format(type(h))
            self._exchange_coefficient = h
        else:
            self._exchange_coefficient = 1.0

    @property
    def isBoundaryLayerPar(self):
        """Return True for isBoundaryLayerPar."""
        return True

    def to_json(self):
        """Create a boundary layer parameter dictionary
        Results:
            {
                day_boundary_layer_height: float positive
                night_boundary_layer_height: float positive
                inversion_height: float positive
                circulation_coefficient: float positive
                exchange_coefficient: float positive
            }
        """
        return {
            "day_boundary_layer_height": self.day_boundary_layer_height,
            "night_boundary_layer_height": self.night_boundary_layer_height,
            "inversion_height": self.inversion_height,
            "circulation_coefficient": self.circulation_coefficient,
            "exchange_coefficient": self.exchange_coefficient
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly boundary layer parameters."""
        return 'Boundary Layer Parameters: ' \
               '\n  Boundary Height (Day | Night): {} m | {} m' \
               '\n  Inversion Height: {} m' \
               '\n  Circulation Coefficient: {}' \
               '\n  Exchange Coefficient: {}'.format(
                   self.day_boundary_layer_height, self.night_boundary_layer_height,
                   self.inversion_height, self.circulation_coefficient,
                   self.exchange_coefficient
                  )
