# coding=utf-8
from __future__ import division

from dfobject import DFParameter
from utilities import Utilities


class TrafficPar(DFParameter):
    """Represents the traffic within an urban area.

    Properties:
        sensible_heat: A number representing the maximum sensible anthropogenic
            heat flux of the urban area in watts per square meter.
        weekday_schedule: A list of 24 fractional values that will be
            multiplied by the sensible_heat to produce hourly values for
            heat on the weekday of the simulation.
            The default is a typical traffic schedule for a commerical area.
        saturday_schedule: A list of 24 fractional values that will be
            multiplied by the sensible_heat to produce hourly values for
            heat on the Saturday of the simulation.
            The default is a typical traffic schedule for a commerical area.
        sunday_schedule: A list of 24 fractional values that will be
            multiplied by the sensible_heat to produce hourly values for
            heat on the Sunday of the simulation.
            The default is a typical traffic schedule for a commerical area.
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
        assert isinstance(heat, (float, int)), \
            'sensible_heat must be a number got {}'.format(type(heat))
        assert (heat >= 0), "sensible_heat must be greater than 0."
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
            self._weekday_schedule = [0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.7, 0.9,
                                      0.9, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.8,
                                      0.9, 0.9, 0.8, 0.8, 0.7, 0.3, 0.2, 0.2]

    @property
    def saturday_schedule(self):
        """Get or set the Saturday traffic schedule."""
        return self._saturday_schedule

    @saturday_schedule.setter
    def saturday_schedule(self, sched):
        if sched != []:
            self._saturday_schedule = self.genChecks.checkSchedule(sched)
        else:
            self._saturday_schedule = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5,
                                       0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.7,
                                       0.7, 0.7, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2]

    @property
    def sunday_schedule(self):
        """Get or set the Sunday traffic schedule as a list."""
        return self._sunday_schedule

    @sunday_schedule.setter
    def sunday_schedule(self, sched):
        if sched != []:
            self._sunday_schedule = self.genChecks.checkSchedule(sched)
        else:
            self._sunday_schedule = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4,
                                     0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
                                     0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2]

    @property
    def isTrafficPar(self):
        """Return True for isTrafficPar."""
        return True

    def get_uwg_matrix(self):
        """A matrix of the traffic schedule that can be assigned to the uwg."""
        return [self.weekday_schedule, self.saturday_schedule, self.sunday_schedule]

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly traffic parameters."""
        return 'Traffic Parameters: ' + \
               '\n  Max Heat: ' + str(self._sensible_heat) + ' W/m2' + \
               '\n  Weekday Avg Heat: ' + str(round(
                   self._sensible_heat * (sum(
                       self._weekday_schedule) / 24), 1)) + ' W/m2' + \
               '\n  Saturday Avg Heat: ' + str(round(
                   self._sensible_heat * (sum(
                       self._saturday_schedule) / 24), 1)) + ' W/m2' + \
               '\n  Sunday Avg Heat: ' + str(round(
                   self._sensible_heat * (sum(
                       self._sunday_schedule) / 24), 1)) + ' W/m2'


class VegetationPar(DFParameter):
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


class PavementPar(DFParameter):
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
