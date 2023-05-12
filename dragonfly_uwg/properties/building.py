# coding=utf-8
"""Building UWG Properties."""
from __future__ import division

from honeybee.typing import float_in_range
from honeybee.altnumber import autocalculate

from ._refdefaults import _RefDefaults


class BuildingUWGProperties(object):
    """UWG Properties for Dragonfly Building.

    Args:
        host: A dragonfly_core Building object that hosts these properties.
        program: Text for the name of the building program. Must be one of the
            options below. (Default: LargeOffice).

            * LargeOffice
            * MediumOffice
            * SmallOffice
            * MidriseApartment
            * Retail
            * StripMall
            * PrimarySchool
            * SecondarySchool
            * SmallHotel
            * LargeHotel
            * Hospital
            * Outpatient
            * Warehouse
            * SuperMarket
            * FullServiceRestaurant
            * QuickServiceRestaurant

        vintage: Text for the vintage of the building. This will be used to set
            default constructions. Must be one of the options below. (Default: New).

            * New
            * 1980_Present
            * Pre1980

        fract_heat_to_canyon: A number from 0 to 1 that represents the fraction of
            the building's waste heat from air conditioning that gets rejected
            into the urban canyon. (Default: 0.5).
        shgc: A number from 0 to 1 that represents the SHGC of the building's windows.
            Used to evaluate the amount of solar heat reflected into the street canyon.
            If autocalculate, it will be set by the building vintage and the Model
            climate zone. (Default: autocalculate).
        wall_albedo: A number from 0 to 1 that represents the exterior wall albedo
            of the building. If autocalculate, it will be set by the building program
            and the DoE commercial reference buildings. (Default: autocalculate).
        roof_albedo: A number from 0 to 1 that represents the exterior roof albedo of
            the building. If autocalculate, it will be set by the vintage, meaning 0.7
            for New and 0.2 for 1980_Present and Pre1980. (Default: autocalculate).
        roof_veg_fraction: A number from 0 to 1 that represents the roof vegetation
            fraction of the building. (Default: 0).

    Properties:
        * host
        * program
        * vintage
        * fract_heat_to_canyon
        * shgc
        * wall_albedo
        * roof_albedo
        * roof_veg_fraction
    """
    __slots__ = ('_host', '_program', '_vintage', '_fract_heat_to_canyon', '_shgc',
                 '_wall_albedo', '_roof_albedo', '_roof_veg_fraction')

    PROGRAMS = \
        ('LargeOffice', 'MediumOffice', 'SmallOffice', 'MidriseApartment', 'Retail',
         'StripMall', 'PrimarySchool', 'SecondarySchool', 'SmallHotel', 'LargeHotel',
         'Hospital', 'Outpatient', 'Warehouse', 'SuperMarket',
         'FullServiceRestaurant', 'QuickServiceRestaurant')
    VINTAGES = ('New', '1980_Present', 'Pre1980')
    _VINTAGE_MAP = {'New': 'new', '1980_Present': 'pst80', 'Pre1980': 'pre80'}

    def __init__(self, host, program='LargeOffice', vintage='New',
                 fract_heat_to_canyon=0.5, shgc=autocalculate, wall_albedo=autocalculate,
                 roof_albedo=autocalculate, roof_veg_fraction=0):
        """Initialize Building UWG properties."""
        self._host = host
        self.program = program
        self.vintage = vintage
        self.fract_heat_to_canyon = fract_heat_to_canyon
        self.shgc = shgc
        self.wall_albedo = wall_albedo
        self.roof_albedo = roof_albedo
        self.roof_veg_fraction = roof_veg_fraction

    @property
    def host(self):
        """Get the Building object hosting these properties."""
        return self._host

    @property
    def program(self):
        """Get or set text for the name of the building program."""
        return self._program

    @program.setter
    def program(self, value):
        assert value in self.PROGRAMS, 'Program "{}" is not acceptable for the UWG. ' \
            'Choose from the following:\n{}'.format(value, '\n'.join(self.PROGRAMS))
        self._program = value

    @property
    def program_uwg(self):
        """Get text for the building program in a format that the UWG likes."""
        if self._program == 'Retail':
            return 'standaloneretail'
        elif self._program == 'MediumOffice':
            return 'medoffice'
        return self._program.lower() 

    @property
    def vintage(self):
        """Get or set text for the vintage of the building."""
        return self._vintage

    @vintage.setter
    def vintage(self, value):
        assert value in self.VINTAGES, 'Vintage "{}" is not acceptable for the UWG. ' \
            'Choose from the following:\n{}'.format(value, '\n'.join(self.VINTAGES))
        self._vintage = value

    @property
    def vintage_uwg(self):
        """Get text for the building vintage in a format that the UWG likes."""
        return self._VINTAGE_MAP[self._vintage]

    @property
    def fract_heat_to_canyon(self):
        """Get or set the fraction of the bldg heat rejected to the urban canyon."""
        return self._fract_heat_to_canyon

    @fract_heat_to_canyon.setter
    def fract_heat_to_canyon(self, value):
        self._fract_heat_to_canyon = float_in_range(value, 0, 1, 'fract_heat_to_canyon')

    @property
    def shgc(self):
        """Get or set the SHGC of the building."""
        return self._shgc if self._shgc is not None else autocalculate

    @shgc.setter
    def shgc(self, value):
        if value == autocalculate:
            self._shgc = None
        else:
            self._shgc = float_in_range(value, 0, 1, 'shgc')

    @property
    def wall_albedo(self):
        """Get or set the exterior wall albedo of the building."""
        if self._wall_albedo is None:
            return _RefDefaults.wall_albedo_by_type(self._program)
        return self._wall_albedo

    @wall_albedo.setter
    def wall_albedo(self, value):
        if value == autocalculate:
            self._wall_albedo = None
        else:
            self._wall_albedo = float_in_range(value, 0, 1, 'wall_albedo')

    @property
    def roof_albedo(self):
        """Get or set the exterior roof albedo of the building."""
        if self._roof_albedo is None:
            return _RefDefaults.roof_albedo_by_era(self._vintage)
        return self._roof_albedo

    @roof_albedo.setter
    def roof_albedo(self, value):
        if value == autocalculate:
            self._roof_albedo = None
        else:
            self._roof_albedo = float_in_range(value, 0, 1, 'roof_albedo')

    @property
    def roof_veg_fraction(self):
        """Get or set the roof vegetation fraction of the building."""
        return self._roof_veg_fraction

    @roof_veg_fraction.setter
    def roof_veg_fraction(self, value):
        self._roof_veg_fraction = float_in_range(value, 0, 1, 'roof_veg_fraction')

    def default_shgc(self, climate_zone):
        """Get the default DoE Reference Building SHGC for this building.

        This is used whenever the building's shgc property is autocalculate.

        Args:
            climate_zone: Text for the ASHRAE climate zone, which must include
                the humidity letter (eg. "4A") unless it is climate zone 7 or 8.
        """
        return _RefDefaults.shgc_by_era_zone(self._vintage, climate_zone)

    def infer_program_from_energy_program(self):
        """Attempt to infer the UWG building program from the honeybee-energy program.

        The inferring will happen by first finding the most common energy ProgramType
        among the assigned Room2Ds. If the identifier of this most common program
        contains the name of an acceptable UWG building program, it will be assigned
        as this object's building program. If no match is found or there's no
        honeybee-energy extension installed, this object's program will remain unchanged.
        """
        try:
            room_progs = [rm.properties.energy.program_type.identifier
                          for rm in self.host.unique_room_2ds]
        except AttributeError:  # dragonfly-energy extension is not installed
            room_progs = None
        if room_progs is not None:
            primary_prog = max(set(room_progs), key=room_progs.count)
            for prog in self.PROGRAMS:
                if prog in primary_prog:
                    self._program = prog
                    break

    @classmethod
    def from_dict(cls, data, host):
        """Create BuildingUWGProperties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of BuildingUWGProperties.
            host: A Building object that hosts these properties.
        """
        assert data['type'] == 'BuildingUWGProperties', \
            'Expected BuildingUWGProperties. Got {}.'.format(data['type'])
        prog, era, f_can, shgc, w_alb, r_alb, r_veg = cls._default_keys(data)
        return cls(host, prog, era, f_can, shgc, w_alb, r_alb, r_veg)

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a BuildingUWGPropertiesAbridged dictionary.

        Args:
            abridged_data: A BuildingUWGPropertiesAbridged dictionary (typically
                coming from a Model).
        """
        prog, era, f_can, shgc, w_alb, r_alb, r_veg = self._default_keys(abridged_data)
        self.program = prog
        self.vintage = era
        self.fract_heat_to_canyon = f_can
        self.shgc = shgc
        self.wall_albedo = w_alb
        self.roof_albedo = r_alb
        self.roof_veg_fraction = r_veg

    def to_dict(self, abridged=False):
        """Return Building UWG properties as a dictionary.

        Args:
            abridged: Boolean for whether the full dictionary of the Building should
                be written (False) or just the identifier of the the individual
                properties (True). Default: False.
        """
        base = {'uwg': {}}
        base['uwg']['type'] = 'BuildingUWGProperties' if not \
            abridged else 'BuildingUWGPropertiesAbridged'

        # write all of the required properties
        base['uwg']['program'] = self._program
        base['uwg']['vintage'] = self._vintage
        base['uwg']['fract_heat_to_canyon'] = self._fract_heat_to_canyon
        base['uwg']['roof_veg_fraction'] = self._roof_veg_fraction

        # write all of the optional properties
        if self._shgc is not None:
            base['uwg']['shgc'] = self._shgc
        if self._wall_albedo is not None:
            base['uwg']['wall_albedo'] = self._wall_albedo
        if self._roof_albedo is not None:
            base['uwg']['roof_albedo'] = self._roof_albedo
        return base

    @staticmethod
    def _default_keys(data):
        prog = data['program'] if 'program' in data else 'LargeOffice'
        era = data['vintage'] if 'vintage' in data else 'New'
        f_can = data['fract_heat_to_canyon'] if 'fract_heat_to_canyon' in data else 0.5
        shgc = autocalculate if 'shgc' not in data or \
            data['shgc'] == autocalculate.to_dict() else data['shgc']
        w_alb = autocalculate if 'wall_albedo' not in data or \
            data['wall_albedo'] == autocalculate.to_dict() else data['wall_albedo']
        r_alb = autocalculate if 'roof_albedo' not in data or \
            data['roof_albedo'] == autocalculate.to_dict() else data['roof_albedo']
        r_veg = data['roof_veg_fraction'] if 'roof_veg_fraction' in data else 0
        return prog, era, f_can, shgc, w_alb, r_alb, r_veg

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new Building object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        _new_obj = BuildingUWGProperties(
            _host, self._program, self._vintage, self._fract_heat_to_canyon)
        _new_obj._shgc = self._shgc
        _new_obj._wall_albedo = self._wall_albedo
        _new_obj._roof_albedo = self._roof_albedo
        _new_obj._roof_veg_fraction = self._roof_veg_fraction
        return _new_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Building UWG Properties: {}'.format(self.host.identifier)
