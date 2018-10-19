# coding=utf-8
from __future__ import division

from utilities import Utilities


class DfParameter(object):
    """Base class for Dragonfly trafficPar, vegetationPar, pavementPar, etc."""

    @property
    def isDfParameter(self):
        """Return True."""
        return True


class TrafficPar(DfParameter):
    """Represents the traffic within an urban area.

    Properties:
        sensible_heat: A number representing the maximum sensible anthropogenic heat flux of the urban area
            in watts per square meter. This input is required.
        weekday_schedule: A list of 24 fractional values that will be multiplied by the sensible_heat
            to produce hourly values for heat on the weekday of the simulation.  The default is
            a typical traffic schedule for a commerical area.
        saturday_schedule: A list of 24 fractional values that will be multiplied by the sensible_heat
            to produce hourly values for heat on Saturdays of the simulation.  The default is
            a typical traffic schedule for a commerical area.
        sunday_schedule: A list of 24 fractional values that will be multiplied by the sensible_heat
            to produce hourly values for heat on Sundays of the simulation.  The default is
            a typical traffic schedule for a commerical area.
    """

    def __init__(self, sensible_heat, weekday_schedule=[],
                 saturday_schedule=[], sunday_schedule=[]):
        """Initialize dragonfly traffic parameters"""
        # get dependencies
        self.genChecks = Utilities()

        self.sensible_heat = sensible_heat
        self.weekday_schedule = weekday_schedule
        self.saturday_schedule = saturday_schedule
        self.sunday_schedule = sunday_schedule

    @property
    def sensible_heat(self):
        """Get or set the max sensible heat flux of the traffic."""
        return self._sensible_heat

    @sensible_heat.setter
    def sensible_heat(self, heat):
        assert isinstance(heat, (float, int)), 'sensible_heat must be a number got {}'.format(type(heat))
        assert (heat >= 0), "sensible_heat must be greater than 0"
        self._sensible_heat = heat

    @property
    def weekday_schedule(self):
        """Get or set the Weekday traffic schedule."""
        return self._weekday_schedule

    @weekday_schedule.setter
    def weekday_schedule(self, sched):
        if sched != []:
            self._weekday_schedule = self.genChecks.checkSchedule(sched)
        else:
            self._weekday_schedule = [0.2,0.2,0.2,0.2,0.2,0.4,0.7,0.9,0.9,0.6,0.6, \
                0.6,0.6,0.6,0.7,0.8,0.9,0.9,0.8,0.8,0.7,0.3,0.2,0.2]

    @property
    def saturday_schedule(self):
        """Get or set the Saturday traffic schedule."""
        return self._saturday_schedule

    @saturday_schedule.setter
    def saturday_schedule(self, sched):
        if sched != []:
            self._saturday_schedule = self.genChecks.checkSchedule(sched)
        else:
            self._saturday_schedule = [0.2,0.2,0.2,0.2,0.2,0.3,0.5,0.5,0.5,0.5,0.5, \
                0.5,0.5,0.5,0.6,0.7,0.7,0.7,0.7,0.5,0.4,0.3,0.2,0.2]

    @property
    def sunday_schedule(self):
        """Get or set the Sunday traffic schedule as a list."""
        return self._sunday_schedule

    @sunday_schedule.setter
    def sunday_schedule(self, sched):
        if sched != []:
            self._sunday_schedule = self.genChecks.checkSchedule(sched)
        else:
            self._sunday_schedule = [0.2,0.2,0.2,0.2,0.2,0.3,0.4,0.4,0.4,0.4,0.4,0.4, \
                0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.3,0.3,0.2,0.2]

    @property
    def isTrafficPar(self):
        """Return True for isTrafficPar."""
        return True

    def get_uwg_matrix(self):
        """Return a python matrix of the traffic schedule that can be assigned to the uwg."""
        return [self.weekday_schedule, self.saturday_schedule, self.sunday_schedule]

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly traffic parameters."""
        return 'Traffic Parameters: ' + \
               '\n  Max Heat: ' + str(self._sensible_heat) + ' W/m2' + \
               '\n  Weekday Avg Heat: ' + str(round(self._sensible_heat* (sum(self._weekday_schedule)/24),1)) + ' W/m2' + \
               '\n  Saturday Avg Heat: ' + str(round(self._sensible_heat* (sum(self._saturday_schedule)/24),1)) + ' W/m2' + \
               '\n  Sunday Avg Heat: ' + str(round(self._sensible_heat* (sum(self._sunday_schedule)/24),1)) + ' W/m2'


class VegetationPar(DfParameter):
    """Represents the behaviour of vegetation within an urban area.

    Properties:
        vegetation_albedo: A number between 0 and 1 that represents the ratio of reflected radiation
            from vegetated surfaces to incident radiation upon them.
        vegetation_start_month: An integer from 1 to 12 that represents the month at which
            vegetation begins to affect the urban climate.  The default is set to 0, which will
            automatically determine the vegetation start month by analyzing the epw to see which
            months have an average monthly temperature above 10 C.
        vegetation_end_month: An integer from 1 to 12 that represents the last month at which
            vegetation affect the urban climate.  The default is set to 0, which will
            automatically determine the vegetation end month by analyzing the epw to see which
            months have an average monthly temperature above 10 C.
        tree_latent_fraction: A number between 0 and 1 that represents the the fraction of absorbed
            solar energy by trees that is given off as latent heat (evapotranspiration). Currently,
            this does not affect the moisture balance in the uwg but it will affect the temperature.
            If no value is input here, a typical value of 0.7 will be assumed.
        grass_latent_fraction: A number between 0 and 1 that represents the the fraction of absorbed solar
            energy by grass that is given off as latent heat (evapotranspiration). Currently,
            this does not affect the moisture balance in the uwg but it will affect the temperature.
            If no value is input here, a typical value of 0.5 will be assumed.
    """

    def __init__(self, vegetation_albedo=0.25, vegetation_start_month=0, vegetation_end_month=0,
                 tree_latent_fraction=0.7, grass_latent_fraction=0.5):
        """Initialize dragonfly vegetation parameters"""
        # get dependencies
        self.genChecks = Utilities()

        self.vegetation_albedo = vegetation_albedo
        self.vegetation_start_month = vegetation_start_month
        self.vegetation_end_month = vegetation_end_month
        self.tree_latent_fraction = tree_latent_fraction
        self.grass_latent_fraction = grass_latent_fraction

        # dictionary of months for start and end month
        self.monthsDict = {
            0: 'Autocalc',
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
            }

    @property
    def vegetation_start_month(self):
        """Get or set the vegetation start month."""
        return self._vegetation_start_month

    @vegetation_start_month.setter
    def vegetation_start_month(self, month):
        if month is not None:
            assert isinstance(month, (float, int)), 'vegetation_start_month must be a number got {}'.format(type(month))
            self._vegetation_start_month = self.genChecks.in_range(int(month), 0, 12, 'vegetation_start_month')
        else:
            self._vegetation_start_month = 0

    @property
    def vegetation_end_month(self):
        """Get or set the vegetation end month."""
        return self._vegetation_end_month

    @vegetation_end_month.setter
    def vegetation_end_month(self, month):
        if month is not None:
            assert isinstance(month, (float, int)), 'vegetation_end_month must be a number got {}'.format(type(month))
            self._vegetation_end_month = self.genChecks.in_range(int(month), 0, 12, 'vegetation_end_month')
        else:
            self._vegetation_end_month = 0

    @property
    def vegetation_albedo(self):
        """Get or set the vegetation albedo."""
        return self._vegetation_albedo

    @vegetation_albedo.setter
    def vegetation_albedo(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), 'vegetation_albedo must be a number got {}'.format(type(a))
            self._vegetation_albedo = self.genChecks.in_range(a, 0, 1, 'vegetation_albedo')
        else:
            self._vegetation_albedo = 0.25

    @property
    def tree_latent_fraction(self):
        """Return the tree latent fraction."""
        return self._tree_latent_fraction

    @tree_latent_fraction.setter
    def tree_latent_fraction(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), 'tree_latent_fraction must be a number got {}'.format(type(a))
            self._tree_latent_fraction = self.genChecks.in_range(a, 0, 1, 'tree_latent_fraction')
        else:
            self._tree_latent_fraction = 0.7

    @property
    def grass_latent_fraction(self):
        """Return the grass latent fraction."""
        return self._grass_latent_fraction

    @grass_latent_fraction.setter
    def grass_latent_fraction(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), 'grass_latent_fraction must be a number got {}'.format(type(a))
            self._grass_latent_fraction = self.genChecks.in_range(a, 0, 1, 'grass_latent_fraction')
        else:
            self._grass_latent_fraction = 0.5

    @property
    def isVegetationPar(self):
        """Return True for isVegetationPar."""
        return True

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly vegetation parameters."""
        return 'Vegetation Parameters: ' + \
               '\n  Albedo: ' + str(self._vegetation_albedo) + \
               '\n  Vegetation Time: ' + self.monthsDict[self._vegetation_start_month] + ' - ' + self.monthsDict[self._vegetation_end_month] + \
               '\n  Tree | Grass Latent: ' + str(self._tree_latent_fraction) + ' | ' + str(self._grass_latent_fraction)


class PavementPar(DfParameter):
    """Represents the makeup of pavement within the urban area.

    Properties:
        albedo: A number between 0 and 1 that represents the surface albedo (or reflectivity)
            of the pavement.  The default is set to 0.1, which is typical of fresh asphalt.
        thickness: A number that represents the thickness of the pavement material in meters (m).
            The default is set to 0.5 meters.
        conductivity: A number representing the conductivity of the pavement material in W/m-K.
            The default is set to 1 W/m-K, which is typical of asphalt.
        volumetric_heat_capacity: A number representing the volumetric heat capacity of
            the pavement material in J/m3-K.  This is the number of joules needed to raise
            one cubic meter of the material by 1 degree Kelvin.  The default is set to
            1,600,000 J/m3-K, which is typical of asphalt.
    """

    def __init__(self, albedo=None, thickness=None, conductivity=None, volumetric_heat_capacity=None):
        """Initialize dragonfly pavement parameters"""
        # get dependencies
        self.genChecks = Utilities()

        self.albedo = albedo
        self.thickness = thickness
        self.conductivity = conductivity
        self.volumetric_heat_capacity = volumetric_heat_capacity

    @property
    def albedo(self):
        """Get or set the road albedo."""
        return self._albedo

    @albedo.setter
    def albedo(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), 'albedo must be a number got {}'.format(type(a))
            self._albedo = self.genChecks.in_range(a, 0, 1, 'albedo')
        else:
            self._albedo = 0.1

    @property
    def thickness(self):
        """Get or set the road thickness."""
        return self._thickness

    @thickness.setter
    def thickness(self, t):
        if t is not None:
            assert isinstance(t, (float, int)), 'thickness must be a number got {}'.format(type(t))
            assert (t >= 0), "thickness must be greater than 0"
            self._thickness = t
        else:
            self._thickness = 0.5

    @property
    def conductivity(self):
        """Get or set the road conductivity."""
        return self._conductivity

    @conductivity.setter
    def conductivity(self, k):
        if k is not None:
            assert isinstance(k, (float, int)), 'conductivity must be a number got {}'.format(type(k))
            assert (k >= 0), "conductivity must be greater than 0"
            self._conductivity = k
        else:
            self._conductivity = 1

    @property
    def volumetric_heat_capacity(self):
        """Get or set the volumetric heat capacity."""
        return self._volumetric_heat_capacity

    @volumetric_heat_capacity.setter
    def volumetric_heat_capacity(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), 'volumetric_heat_capacity must be a number got {}'.format(type(x))
            assert (x >= 0), "volumetric_heat_capacity must be greater than 0"
            self._volumetric_heat_capacity = x
        else:
            self._volumetric_heat_capacity = 1600000

    @property
    def isPavementPar(self):
        """Return True for isPavementPar."""
        return True

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly pavement parameters."""
        return 'Pavement Parameters: ' + \
               '\n  Albedo: ' + str(self._albedo) + \
               '\n  Thickness: ' + str(self._thickness) + \
               '\n  Conductivity: ' + str(self._conductivity) + \
               '\n  Vol Heat Capacity: ' + str(self._volumetric_heat_capacity)


class RefEPWSitePar(DfParameter):
    """Represents the properties of the reference site where the original EPW was recorded.

    Properties:
        average_obstacle_height: A number that represents the height in meters of objects that
            obstruct the view to the sky at the weather station site.  This includes both trees
            and buildings.  The default is set to 0.1 meters.
        vegetation_coverage: A number between 0 and 1 that represents that fraction of the reference
            EPW site that is covered in grass. If nothing is input here, a defailt of 0.9 will be used.
        temp_measure_height: A number that represents the height in meters at which temperature is
            measured on the weather station.  The default is set to 10 meters as this is the standard
            measurement height for US Department of Energy EPW files.
        wind_measure_height: A number that represents the height in meters at which wind speed is
            measured on the weather station.  The default is set to 10 meters as this is the standard
            measurement height for US Department of Energy EPW files.
    """

    def __init__(self, average_obstacle_height=None, vegetation_coverage=None, temp_measure_height=None, wind_measure_height=None):
        """Initialize RefEPWSitePar parameters"""
        # get dependencies
        self.genChecks = Utilities()

        self.average_obstacle_height = average_obstacle_height
        self.vegetation_coverage = vegetation_coverage
        self.temp_measure_height = temp_measure_height
        self.wind_measure_height = wind_measure_height

    @property
    def average_obstacle_height(self):
        """Get or set the average obstacle height."""
        return self._average_obstacle_height

    @average_obstacle_height.setter
    def average_obstacle_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), 'average_obstacle_height must be a number got {}'.format(type(h))
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
            assert isinstance(a, (float, int)), 'vegetation_coverage must be a number got {}'.format(type(a))
            self._vegetation_coverage = self.genChecks.in_range(a, 0, 1, 'vegetation_coverage')
        else:
            self._vegetation_coverage = 0.9

    @property
    def temp_measure_height(self):
        """Get or set the temperature measurement height."""
        return self._temp_measure_height

    @temp_measure_height.setter
    def temp_measure_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), 'temp_measure_height must be a number got {}'.format(type(h))
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
            assert isinstance(h, (float, int)), 'wind_measure_height must be a number got {}'.format(type(h))
            assert (h >= 0), "wind_measure_height must be greater than 0"
            self._wind_measure_height = h
        else:
            self._wind_measure_height = 10

    @property
    def isRefEPWSitePar(self):
        """Return True for isRefEPWSitePar."""
        return True

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly reference EPW site parameters."""
        return 'Reference EPW Site Parameters: ' + \
               '\n  Obstacle Height: ' + str(self._average_obstacle_height) + ' m' + \
               '\n  Vegetation Coverage: ' + str(self._vegetation_coverage) + \
               '\n  Measurement Height (Temp | Wind): ' + str(self._temp_measure_height) + \
                    ' m | ' + str(self._wind_measure_height) + ' m'


class BoundaryLayerPar(DfParameter):
    """Represents the properties of the urban boundary layer.

    Properties:
        day_boundary_layer_height: A number that represents the height in meters of the urban boundary layer
            during the daytime. This is the height to which the urban meterorological conditions are stable
            and representative of the overall urban area. Typically, this boundary layer height increases with
            the height of the buildings.  The default is set to 1000 meters.
        night_boundary_layer_height: A number that represents the height in meters of the urban boundary layer
            during the nighttime. This is the height to which the urban meterorological conditions are stable
            and representative of the overall urban area. Typically, this boundary layer height increases with
            the height of the buildings.  The default is set to 80 meters.
        inversion_height: A number that represents the height at which the vertical profile of potential
            temperature becomes stable. It is the height at which the profile of air temperature becomes
            stable. Can be determined by flying helium balloons equipped with temperature sensors and
            recording the air temperatures at different heights.  The default is set to 150 meters.
        circulation_coefficient: A number that represents the circulation coefficient.  The default
            is 1.2 per Bueno, Bruno (2012).
        exchange_coefficient: A number that represents the exchange coefficient.  The default is
            1.0 per Bueno, Bruno (2014).
    """

    def __init__(self, day_boundary_layer_height=None, night_boundary_layer_height=None,
                 inversion_height=None, circulation_coefficient=None, exchange_coefficient=None):
        """Initialize Boundary Layer parameters"""

        self.day_boundary_layer_height = day_boundary_layer_height
        self.night_boundary_layer_height = night_boundary_layer_height
        self.inversion_height = inversion_height
        self.circulation_coefficient = circulation_coefficient
        self.exchange_coefficient = exchange_coefficient

    @property
    def day_boundary_layer_height(self):
        """Get or set the daytime boundary layer height."""
        return self._day_boundary_layer_height

    @day_boundary_layer_height.setter
    def day_boundary_layer_height(self, h):
        if h is not None:
            assert isinstance(h, (float, int)), 'day_boundary_layer_height must be a number got {}'.format(type(h))
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
            assert isinstance(h, (float, int)), 'night_boundary_layer_height must be a number got {}'.format(type(h))
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
            assert isinstance(h, (float, int)), 'inversion_height must be a number got {}'.format(type(h))
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
            assert isinstance(h, (float, int)), 'circulation_coefficient must be a number got {}'.format(type(h))
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
            assert isinstance(h, (float, int)), 'exchange_coefficient must be a number got {}'.format(type(h))
            self._exchange_coefficient = h
        else:
            self._exchange_coefficient = 1.0

    @property
    def isBoundaryLayerPar(self):
        """Return True for isBoundaryLayerPar."""
        return True

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly boundary layer parameters."""
        return 'Boundary Layer Parameters: ' + \
               '\n  Boundary Height (Day | Night): ' + str(self.day_boundary_layer_height) + \
                    ' m | ' + str(self.night_boundary_layer_height) + ' m' +\
               '\n  Inversion Height: ' + str(self.inversion_height) + ' m' + \
               '\n  Circulation Coefficient: ' + str(self.circulation_coefficient) + \
               '\n  Exchange Coefficient: ' + str(self.exchange_coefficient)
