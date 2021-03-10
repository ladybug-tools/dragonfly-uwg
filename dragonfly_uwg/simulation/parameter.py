# coding=utf-8
"""Complete set of UWG Simulation Settings."""
from __future__ import division

from .runperiod import UWGRunPeriod
from .vegetation import VegetationParameter
from .refsite import ReferenceEPWSite
from .boundary import BoundaryLayerParameter

from honeybee.altnumber import autocalculate
from honeybee.typing import int_positive
from ladybug.epw import EPW


class UWGSimulationParameter(object):
    """Complete set of UWG Simulation Settings.

    Args:
        climate_zone: Text for the ASHRAE climate zone, including the letter for
            humidity classification (eg. "4A"). This is used to set default
            constructions for various buildings. If set to autocalculate,
            the climate zone will be estimated from analysis of the epw to be
            morphed for simulation. (Default: autocalculate).
        run_period: A UWGRunPeriod object to describe the time period over which to
            run the simulation. If None, the simulation will be run for the whole
            year. (Default: None).
        timestep: An integer for the number of timesteps per hour at which the
            calculation will be run. (Default: 12).
        vegetation_parameter: A VegetationParameter to specify the behavior of
            vegetation in the urban area. If None, generic vegetation parameters
            will be generated. (Default: None).
        reference_epw_site: A ReferenceEPWSite to specify the properties of the
            reference site where the input rural EPW was recorded. If None, generic
            airport properties will be generated. (Default: None).
        boundary_layer_parameter: A BoundaryLayerParameter to specify the properties
            of the urban boundary layer. If None, generic boundary layer parameters
            will be generated. (Default: None).
    """
    __slots__ = ('_climate_zone', '_run_period', '_timestep', '_vegetation_parameter',
                 '_reference_epw_site', '_boundary_layer_parameter')

    VALIDTIMESTEPS = (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60)
    VALIDZONES = ('1A', '2A', '2B', '3A', '3B', '3C', '4A', '4B', '4C',
                  '5A', '5B', '6A', '6B', '7', '8')

    def __init__(self, climate_zone=autocalculate, run_period=None, timestep=12,
                 vegetation_parameter=None, reference_epw_site=None,
                 boundary_layer_parameter=None):
        """Initialize UWGSimulationParameter"""
        self.climate_zone = climate_zone
        self.run_period = run_period
        self.timestep = timestep
        self.vegetation_parameter = vegetation_parameter
        self.reference_epw_site = reference_epw_site
        self.boundary_layer_parameter = boundary_layer_parameter

    @property
    def climate_zone(self):
        """Get or set a text for the ASHRAE climate zone."""
        return self._climate_zone if self._climate_zone is not None else autocalculate

    @climate_zone.setter
    def climate_zone(self, value):
        if value == autocalculate:
            self._climate_zone = None
        else:
            assert value in self.VALIDZONES, 'UWGSimulationParameter climate_zone ' \
                '"{}" is invalid.\nMust be one of the following:{}'.format(
                    value, self.VALIDZONES)
            self._climate_zone = value

    @property
    def run_period(self):
        """Get or set a UWGRunPeriod object for the time period to run the simulation."""
        return self._run_period

    @run_period.setter
    def run_period(self, value):
        if value is not None:
            assert isinstance(value, UWGRunPeriod), 'Expected UWGRunPeriod for ' \
                'UWGSimulationParameter run_period. Got {}.'.format(type(value))
            self._run_period = value
        else:
            self._run_period = UWGRunPeriod()

    @property
    def timestep(self):
        """Get or set a integer for the number of simulation timesteps per hour."""
        return self._timestep

    @timestep.setter
    def timestep(self, value):
        value = int_positive(value, 'simulation parameter timestep')
        assert value in self.VALIDTIMESTEPS, 'UWGSimulationParameter timestep "{}" is ' \
            'invalid. Must be one of the following:{}'.format(value, self.VALIDTIMESTEPS)
        self._timestep = value

    @property
    def vegetation_parameter(self):
        """Get or set a VegetationParameter object for the behavior of vegetation."""
        return self._vegetation_parameter

    @vegetation_parameter.setter
    def vegetation_parameter(self, value):
        if value is not None:
            assert isinstance(value, VegetationParameter), 'Expected ' \
                'VegetationParameter. Got {}.'.format(type(value))
            self._vegetation_parameter = value
        else:
            self._vegetation_parameter = VegetationParameter()

    @property
    def reference_epw_site(self):
        """Get or set a ReferenceEPWSite object for the properties of the rural EPW."""
        return self._reference_epw_site

    @reference_epw_site.setter
    def reference_epw_site(self, value):
        if value is not None:
            assert isinstance(value, ReferenceEPWSite), 'Expected ReferenceEPWSite ' \
                'for UWGSimulationParameter. Got {}.'.format(type(value))
            self._reference_epw_site = value
        else:
            self._reference_epw_site = ReferenceEPWSite()

    @property
    def boundary_layer_parameter(self):
        """Get or set a BoundaryLayerParameter object for the boundary layer properties.
        """
        return self._boundary_layer_parameter

    @boundary_layer_parameter.setter
    def boundary_layer_parameter(self, value):
        if value is not None:
            assert isinstance(value, BoundaryLayerParameter), 'Expected ' \
                'BoundaryLayerParameter. Got {}.'.format(type(value))
            self._boundary_layer_parameter = value
        else:
            self._boundary_layer_parameter = BoundaryLayerParameter()

    @classmethod
    def from_dict(cls, data):
        """Create a UWGSimulationParameter object from a dictionary.

        Args:
            data: A UWGSimulationParameter dictionary in following the format below.

        .. code-block:: python

            {
            "type": "UWGSimulationParameter",
            "climate_zone": "5A",  # Text for ASHRAE climate zone
            "run_period": {}, # Dragonfly UWGRunPeriod dictionary
            "timestep": 20, # Integer for the simulation timestep
            "vegetation_parameter": {}, # Dragonfly VegetationParameter dictionary
            "reference_epw_site": {}, # Dragonfly ReferenceEPWSite dictionary
            "boundary_layer_parameter": {} # Dragonfly BoundaryLayerParameter dictionary
            }
        """
        assert data['type'] == 'UWGSimulationParameter', \
            'Expected UWGSimulationParameter dictionary. Got {}.'.format(data['type'])

        cz = autocalculate if 'climate_zone' not in data or \
            data['climate_zone'] == autocalculate.to_dict() else data['climate_zone']
        timestep = data['timestep'] if 'timestep' in data else 12
        run_period = None
        if 'run_period' in data and data['run_period'] is not None:
            run_period = UWGRunPeriod.from_dict(data['run_period'])
        veg_par = None
        if 'vegetation_parameter' in data and data['vegetation_parameter'] is not None:
            veg_par = VegetationParameter.from_dict(data['vegetation_parameter'])
        ref_site = None
        if 'reference_epw_site' in data and data['reference_epw_site'] is not None:
            ref_site = ReferenceEPWSite.from_dict(data['reference_epw_site'])
        bnd_par = None
        if 'boundary_layer_parameter' in data and \
                data['boundary_layer_parameter'] is not None:
            bnd_par = BoundaryLayerParameter.from_dict(data['boundary_layer_parameter'])

        return cls(cz, run_period, timestep, veg_par, ref_site, bnd_par)

    def to_dict(self):
        """UWGSimulationParameter dictionary representation."""
        base = {
            'type': 'UWGSimulationParameter',
            'run_period': self.run_period.to_dict(),
            'timestep': self.timestep,
            'vegetation_parameter': self.vegetation_parameter.to_dict(),
            'reference_epw_site': self.reference_epw_site.to_dict(),
            'boundary_layer_parameter': self.boundary_layer_parameter.to_dict()}
        if self._climate_zone is not None:
            base['climate_zone'] = self.climate_zone
        return base

    def to_uwg_dict(self, epw_file):
        """Get a dictionary following the input schema of the UWG.

        Note that this dictionary will only include the properties that the
        UWGSimulationParameter object possesses and will lack all of those provided
        by the Model object. For fully simulate-able UWG input, the Model.to.uwg
        method should be used. The keys of the dictionary output by this method
        include the following.

        * zone
        * month
        * day
        * nday
        * dtsim
        * rurvegcover
        * vegstart
        * vegend
        * albveg
        * latgrss
        * lattree
        * h_ubl1
        * h_ubl2
        * h_ref
        * h_temp
        * h_wind
        * c_circ
        * c_exch
        * h_obs

        Args:
            epw_file: File path to the EPW that will be morphed by the UWG. This
                will be used to fill all autocalculated fields like the ASHRAE
                climate zone and vegetation start/end.
        """
        # autocalculate any missing values from the epw_file
        climate_zone = self._climate_zone
        veg_start = self.vegetation_parameter._start_month
        veg_end = self.vegetation_parameter._end_month
        if climate_zone is None or veg_start is None or veg_end is None:
            epw_obj = EPW(epw_file)
            start_def, end_def = self._autocalc_start_end_vegetation(epw_obj)
            veg_start = start_def if veg_start is None else veg_start
            veg_end = end_def if veg_end is None else veg_end
            climate_zone = epw_obj.ashrae_climate_zone if climate_zone is None \
                else climate_zone

        # create the uwg dictionary
        base = {}
        base['zone'] = climate_zone
        base['month'] = self.run_period.start_date.month
        base['day'] = self.run_period.start_date.day
        base['nday'] = self.run_period.day_count
        base['dtsim'] = int((60 / self.timestep) * 60)
        base['vegstart'] = veg_start
        base['vegend'] = veg_end
        base['albveg'] = self.vegetation_parameter.vegetation_albedo
        base['latgrss'] = self.vegetation_parameter.grass_latent_fraction
        base['lattree'] = self.vegetation_parameter.tree_latent_fraction
        base['h_ubl1'] = self.boundary_layer_parameter.day_boundary_layer_height
        base['h_ubl2'] = self.boundary_layer_parameter.night_boundary_layer_height
        base['h_ref'] = self.boundary_layer_parameter.inversion_height
        base['c_circ'] = self.boundary_layer_parameter.circulation_coefficient
        base['c_exch'] = self.boundary_layer_parameter.exchange_coefficient
        base['rurvegcover'] = self.reference_epw_site.vegetation_coverage
        base['h_temp'] = self.reference_epw_site.temp_measure_height
        base['h_wind'] = self.reference_epw_site.wind_measure_height
        base['h_obs'] = self.reference_epw_site.average_obstacle_height
        return base

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    @staticmethod
    def _autocalc_start_end_vegetation(epw_obj, threshold_temp=10):
        """Autocalculate the vegetation start and end month from an EPW."""
        month_temps = epw_obj.dry_bulb_temperature.average_monthly()
        veg_start, veg_end, veg_start_set = 1, 12, False
        for i, t in enumerate(month_temps):
            if t > threshold_temp and not veg_start_set:
                veg_start, veg_start_set = i + 1, True
            elif t < threshold_temp and veg_start_set:
                veg_end, veg_start_set = i + 1, False
        return veg_start, veg_end

    def __copy__(self):
        return UWGSimulationParameter(
            self.climate_zone, self.run_period.duplicate(), self.timestep,
            self.vegetation_parameter.duplicate(), self.reference_epw_site.duplicate(),
            self.boundary_layer_parameter.duplicate())

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        return 'UWG SimulationParameter:'
