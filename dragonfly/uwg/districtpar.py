# coding=utf-8
from __future__ import division

from ..dfobject import DFParameter
from ..utilities import in_range


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
        self.sensible_heat = sensible_heat
        self.weekday_schedule = weekday_schedule
        self.saturday_schedule = saturday_schedule
        self.sunday_schedule = sunday_schedule

    @classmethod
    def from_json(cls, data):
        """Create a traffic parameter object from a dictionary
        Args:
            data: {
                sensible_heat: float
                weekday_schedule: [] list of 24 fractional values
                saturday_schedule: [] list of 24 fractional values
                sunday_schedule: [] list of 24 fractional values
            }
        """

        required_keys = ("sensible_heat",)
        nullable_keys = ("weekday_schedule", "saturday_schedule",
                         "sunday_schedule")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(sensible_heat=data["sensible_heat"],
                   weekday_schedule=data["weekday_schedule"],
                   saturday_schedule=data["saturday_schedule"],
                   sunday_schedule=data["sunday_schedule"])

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
            self._weekday_schedule = self._checkSchedule(sched)
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
            self._saturday_schedule = self._checkSchedule(sched)
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
            self._sunday_schedule = self._checkSchedule(sched)
        else:
            self._sunday_schedule = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4,
                                     0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
                                     0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2]

    @property
    def weekday_hourly_heat(self):
        """Get a list of W/m2 on each hour of the Weekday."""
        return [frac * self._sensible_heat for frac in self._weekday_schedule]

    @property
    def saturday_hourly_heat(self):
        """Get a list of W/m2 on each hour of the Saturday."""
        return [frac * self._sensible_heat for frac in self._saturday_schedule]

    @property
    def sunday_hourly_heat(self):
        """Get a list of W/m2 on each hour of the Sunday."""
        return [frac * self._sensible_heat for frac in self._sunday_schedule]

    @property
    def weekday_avg_heat(self):
        """Get the average W/m2 over the Weekday."""
        return sum(self.weekday_hourly_heat) / 24

    @property
    def saturday_avg_heat(self):
        """Get the average W/m2 over the Saturday."""
        return sum(self.saturday_hourly_heat) / 24

    @property
    def sunday_avg_heat(self):
        """Get the average W/m2 over the Sunday."""
        return sum(self.sunday_hourly_heat) / 24

    @property
    def isTrafficPar(self):
        """Return True for isTrafficPar."""
        return True

    def get_uwg_matrix(self):
        """A matrix of the traffic schedule that can be assigned to the uwg."""
        return [self.weekday_schedule, self.saturday_schedule, self.sunday_schedule]

    def _checkSchedule(self, schedule):
        if len(schedule) == 24:
            return [in_range(x, 0, 1, 'schedule value') for x in schedule]
        else:
            raise Exception(
                "Current schedule has length " + str(len(schedule)) +
                ". Daily schedules must be lists of 24 values."
            )

    def to_json(self):
        """Create a traffic parameter dictionary
        Returns:
            {
                sensible_heat: float
                weekday_schedule: [] list of 24 fractional values
                saturday_schedule: [] list of 24 fractional values
                sunday_schedule: [] list of 24 fractional values
            }
        """
        return {
            "sensible_heat": self.sensible_heat,
            "weekday_schedule": self.weekday_schedule,
            "saturday_schedule": self.saturday_schedule,
            "sunday_schedule": self.sunday_schedule
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly traffic parameters."""
        return 'Traffic Parameters: ' \
               '\n  Max Heat: {} W/m2' \
               '\n  Weekday Avg Heat: {} W/m2' \
               '\n  Saturday Avg Heat: {} W/m2' \
               '\n  Sunday Avg Heat: {} W/m2'.format(
                   self._sensible_heat, self.weekday_avg_heat,
                   self.saturday_avg_heat, self.sunday_avg_heat
               )


class VegetationPar(DFParameter):
    """Represents the behaviour of vegetation within an urban area.

    Properties:
        vegetation_albedo: A number between 0 and 1 that represents
            the ratio of reflected radiation from vegetated surfaces
            to incident radiation upon them.
        vegetation_start_month: An integer from 1 to 12 that represents
            the month at which vegetation begins to affect the urban climate.
            The default is set to 0, which will automatically determine the
            vegetation start month by analyzing the epw to see which
            months have an average monthly temperature above 10 C.
        vegetation_end_month: An integer from 1 to 12 that represents
            the last month at which vegetation affect the urban climate.
            The default is set to 0, which will automatically determine
            the vegetation end month by analyzing the epw to see which
            months have an average monthly temperature above 10 C.
        tree_latent_fraction: A number between 0 and 1 that represents
            the the fraction of absorbed solar energy by trees that
            is given off as latent heat (evapotranspiration). Currently,
            this does not affect the moisture balance in the uwg but
            it will affect the temperature.
            If no value is input here, a typical value of 0.7 will be assumed.
        grass_latent_fraction: A number between 0 and 1 that represents
            the the fraction of absorbed solar energy by grass that is
            given off as latent heat (evapotranspiration). Currently,
            this does not affect the moisture balance in the uwg but
            it will affect the temperature.
            If no value is input here, a typical value of 0.5 will be assumed.
    """

    def __init__(self, vegetation_albedo=0.25,
                 vegetation_start_month=0, vegetation_end_month=0,
                 tree_latent_fraction=0.7, grass_latent_fraction=0.5):
        """Initialize dragonfly vegetation parameters"""
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

    @classmethod
    def from_json(cls, data):
        """Create a vegetation parameter object from a dictionary
        Args:
            data: {
                vegetation_albedo: float between 0 and 1
                vegetation_start_month: int between 0 and 12
                vegetation_end_month: int between 0 and 12
                tree_latent_fraction: float between 0 and 1
                grass_latent_fraction: float between 0 and 1
            }
        """

        required_keys = ()
        nullable_keys = ("vegetation_albedo", "vegetation_start_month",
                         "vegetation_end_month", "tree_latent_fraction",
                         "grass_latent_fraction")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(vegetation_albedo=data["vegetation_albedo"],
                   vegetation_start_month=data["vegetation_start_month"],
                   vegetation_end_month=data["vegetation_end_month"],
                   tree_latent_fraction=data["tree_latent_fraction"],
                   grass_latent_fraction=data["grass_latent_fraction"])

    @property
    def vegetation_start_month(self):
        """Get or set the vegetation start month."""
        return self._vegetation_start_month

    @vegetation_start_month.setter
    def vegetation_start_month(self, month):
        if month is not None:
            assert isinstance(month, (float, int)), \
                'vegetation_start_month must be a number got {}'.format(type(month))
            self._vegetation_start_month = in_range(
                int(month), 0, 12, 'vegetation_start_month')
        else:
            self._vegetation_start_month = 0

    @property
    def veg_start_month_text(self):
        """The text name of the vegetation start month."""
        return self.monthsDict[self._vegetation_start_month]

    @property
    def vegetation_end_month(self):
        """Get or set the vegetation end month."""
        return self._vegetation_end_month

    @vegetation_end_month.setter
    def vegetation_end_month(self, month):
        if month is not None:
            assert isinstance(month, (float, int)), \
                'vegetation_end_month must be a number got {}'.format(type(month))
            self._vegetation_end_month = in_range(
                int(month), 0, 12, 'vegetation_end_month')
        else:
            self._vegetation_end_month = 0

    @property
    def veg_end_month_text(self):
        """The text name of the vegetation end month."""
        return self.monthsDict[self._vegetation_end_month]

    @property
    def vegetation_albedo(self):
        """Get or set the vegetation albedo."""
        return self._vegetation_albedo

    @vegetation_albedo.setter
    def vegetation_albedo(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), \
                'vegetation_albedo must be a number got {}'.format(type(a))
            self._vegetation_albedo = in_range(
                a, 0, 1, 'vegetation_albedo')
        else:
            self._vegetation_albedo = 0.25

    @property
    def tree_latent_fraction(self):
        """Return the tree latent fraction."""
        return self._tree_latent_fraction

    @tree_latent_fraction.setter
    def tree_latent_fraction(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), \
                'tree_latent_fraction must be a number got {}'.format(type(a))
            self._tree_latent_fraction = in_range(
                a, 0, 1, 'tree_latent_fraction')
        else:
            self._tree_latent_fraction = 0.7

    @property
    def grass_latent_fraction(self):
        """Return the grass latent fraction."""
        return self._grass_latent_fraction

    @grass_latent_fraction.setter
    def grass_latent_fraction(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), \
                'grass_latent_fraction must be a number got {}'.format(type(a))
            self._grass_latent_fraction = in_range(
                a, 0, 1, 'grass_latent_fraction')
        else:
            self._grass_latent_fraction = 0.5

    @property
    def isVegetationPar(self):
        """Return True for isVegetationPar."""
        return True

    def to_json(self):
        """Create a vegetation parameter dictionary
        Returns:
            {
                vegetation_albedo: float between 0 and 1
                vegetation_start_month: int between 0 and 11
                vegetation_end_month: int between 0 and 11
                tree_latent_fraction: float between 0 and 1
                grass_latent_fraction: float between 0 and 1
            }
        """
        return {
            "vegetation_albedo": self.vegetation_albedo,
            "vegetation_start_month": self.vegetation_start_month,
            "vegetation_end_month": self.vegetation_end_month,
            "tree_latent_fraction": self.tree_latent_fraction,
            "grass_latent_fraction": self.grass_latent_fraction
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly vegetation parameters."""
        return 'Vegetation Parameters: ' \
               '\n  Albedo: {}' \
               '\n  Vegetation Time: {} - {}' \
               '\n  Tree | Grass Latent: {} | {}'.format(
                   self._vegetation_albedo,
                   self.veg_start_month_text, self.veg_end_month_text,
                   self._tree_latent_fraction, self._grass_latent_fraction
               )


class PavementPar(DFParameter):
    """Represents the makeup of pavement within the urban area.

    Properties:
        albedo: A number between 0 and 1 that represents the
            surface albedo (or reflectivity) of the pavement.
            The default is set to 0.1, which is typical of fresh asphalt.
        thickness: A number that represents the thickness of the
            pavement material in meters (m).
            The default is set to 0.5 meters.
        conductivity: A number representing the conductivity
            of the pavement material in W/m-K.
            The default is set to 1 W/m-K, which is typical of asphalt.
        volumetric_heat_capacity: A number representing the
            volumetric heat capacity of the pavement material in J/m3-K.
            This is the number of joules needed to raise
            one cubic meter of the material by 1 degree Kelvin.
            The default is set to 1,600,000 J/m3-K, which is typical of asphalt.
    """

    def __init__(self, albedo=None, thickness=None,
                 conductivity=None, volumetric_heat_capacity=None):
        """Initialize dragonfly pavement parameters"""
        self.albedo = albedo
        self.thickness = thickness
        self.conductivity = conductivity
        self.volumetric_heat_capacity = volumetric_heat_capacity

    @classmethod
    def from_json(cls, data):
        """Create a pavement parameter object from a dictionary
        Args:
            data: {
                albedo: float between 0 and 1
                thickness: float positive
                conductivity: float positive
                volumetric_heat_capacity: float positive
            }
        """

        required_keys = ()
        nullable_keys = ("albedo", "thickness", "conductivity",
                         "volumetric_heat_capacity")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(albedo=data["albedo"],
                   thickness=data["thickness"],
                   conductivity=data["conductivity"],
                   volumetric_heat_capacity=data["volumetric_heat_capacity"])

    @property
    def albedo(self):
        """Get or set the road albedo."""
        return self._albedo

    @albedo.setter
    def albedo(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), \
                'albedo must be a number got {}'.format(type(a))
            self._albedo = in_range(a, 0, 1, 'albedo')
        else:
            self._albedo = 0.1

    @property
    def thickness(self):
        """Get or set the road thickness."""
        return self._thickness

    @thickness.setter
    def thickness(self, t):
        if t is not None:
            assert isinstance(t, (float, int)), \
                'thickness must be a number got {}'.format(type(t))
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
            assert isinstance(k, (float, int)), \
                'conductivity must be a number got {}'.format(type(k))
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
            assert isinstance(x, (float, int)), \
                'volumetric_heat_capacity must be a number got {}'.format(type(x))
            assert (x >= 0), "volumetric_heat_capacity must be greater than 0"
            self._volumetric_heat_capacity = x
        else:
            self._volumetric_heat_capacity = 1600000

    @property
    def isPavementPar(self):
        """Return True for isPavementPar."""
        return True

    def to_json(self):
        """Create a pavement parameter dictionary
        Results:
            {
                albedo: float between 0 and 1
                thickness: float positive
                conductivity: float positive
                volumetric_heat_capacity: float positive
            }
        """
        return {
            "albedo": self.albedo,
            "thickness": self.thickness,
            "conductivity": self.conductivity,
            "volumetric_heat_capacity": self.volumetric_heat_capacity
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly pavement parameters."""
        return 'Pavement Parameters: ' \
               '\n  Albedo: {}' \
               '\n  Thickness: {}' \
               '\n  Conductivity: {}' \
               '\n  Vol Heat Capacity: {}'.format(
                   self._albedo, self._thickness,
                   self._conductivity, self._volumetric_heat_capacity
               )
