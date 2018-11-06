# coding=utf-8
from __future__ import division

from ..dfobject import DFParameter
from ..utilities import in_range


class TypologyPar(DFParameter):
    """Represents the properties of a building typology that relate to the UWG.

    Properties:
        fract_heat_to_canyon: A number from 0 to 1 that represents the fraction
            the building's waste heat from air conditioning that gets rejected
            into the urban canyon. The default is set to 0.5.
        shgc: A number from 0 to 1 that represents the SHGC of the
            buildings in the typology.
        wall_albedo: A number from 0 to 1 that represents the exterior
            wall albedo of the buildings in the typology.
            The default is taken from the DOE commercial building reference
            and varies by building typology type.
        roof_albedo: A number from 0 to 1 that represents the exterior
            roof albedo of the buildings in the typology.
            The default is 0.7 for NewConstruction and 0.2 for
            Pre1980s and 1980sPresent.
        roof_veg_fraction: A number from 0 to 1 that represents the
            roof vegetation fraction of the buildings in the typology.
    """

    def __init__(self, fract_heat_to_canyon=None, shgc=None,
                 wall_albedo=None, roof_albedo=None, roof_veg_fraction=None):
        """Initialize uwg typology parameters"""
        self.fract_heat_to_canyon = fract_heat_to_canyon
        self.shgc = shgc
        self.wall_albedo = wall_albedo
        self.roof_albedo = roof_albedo
        self.roof_veg_fraction = roof_veg_fraction

    @classmethod
    def from_json(cls, data):
        """Create a typology parameter object from a dictionary
        Args:
            data: {
                fract_heat_to_canyon: float between 0 and 1
                shgc: float
                wall_albedo: float between 0 and 1
                roof_albedo: float between 0 and 1
                roof_veg_fraction: float between 0 and 1
            }
        """

        required_keys = ()
        nullable_keys = ("fract_heat_to_canyon", "shgc",
                         "wall_albedo", "roof_albedo", "roof_veg_fraction")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(fract_heat_to_canyon=data["fract_heat_to_canyon"],
                   shgc=data["shgc"],
                   wall_albedo=data["wall_albedo"],
                   roof_albedo=data["roof_albedo"],
                   roof_veg_fraction=data["roof_veg_fraction"])

    @property
    def fract_heat_to_canyon(self):
        """Get or set the fraction of the bldg heat rejected to the urban canyon."""
        return self._fract_heat_to_canyon

    @fract_heat_to_canyon.setter
    def fract_heat_to_canyon(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'fract_heat_to_canyon must be a number got {}'.format(type(x))
            self._fract_heat_to_canyon = in_range(
                x, 0, 1, 'fract_heat_to_canyon')
        else:
            self._fract_heat_to_canyon = 0.5

    @property
    def shgc(self):
        """Get or set the SHGC of the buildings in the typology."""
        return self._shgc

    @shgc.setter
    def shgc(self, x):
        self._shgc = None
        if x is not None:
            assert isinstance(x, (float, int)), \
                'shgc must be a number got {}'.format(type(x))
            self._shgc = in_range(x, 0, 1, 'shgc')

    @property
    def wall_albedo(self):
        """Get or set the exterior wall albedo of the buildings in the typology."""
        return self._wall_albedo

    @wall_albedo.setter
    def wall_albedo(self, x):
        self._wall_albedo = None
        if x is not None:
            assert isinstance(x, (float, int)), \
                'wall_albedo must be a number got {}'.format(type(x))
            self._wall_albedo = in_range(x, 0, 1, 'wall_albedo')

    @property
    def roof_albedo(self):
        """Get or set the exterior roof albedo of the buildings in the typology."""
        return self._roof_albedo

    @roof_albedo.setter
    def roof_albedo(self, x):
        self._roof_albedo = None
        if x is not None:
            assert isinstance(x, (float, int)), \
                'roof_albedo must be a number got {}'.format(type(x))
            self._roof_albedo = in_range(x, 0, 1, 'roof_albedo')

    @property
    def roof_veg_fraction(self):
        """Get or set the roof vegetation fraction of the buildings in the typology."""
        return self._roof_veg_fraction

    @roof_veg_fraction.setter
    def roof_veg_fraction(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'roof_veg_fraction must be a number got {}'.format(type(x))
            self._roof_veg_fraction = in_range(x, 0, 1, 'roof_veg_fraction')
        else:
            self._roof_veg_fraction = 0.

    @property
    def isTypologyPar(self):
        """Return True for isTypologyPar."""
        return True

    def to_json(self):
        """Create a typology parameter dictionary
        Returns:
            {
                fract_heat_to_canyon: float between 0 and 1
                shgc: float
                wall_albedo: float between 0 and 1
                roof_albedo: float between 0 and 1
                roof_veg_fraction: float between 0 and 1
            }
        """
        return {
            "fract_heat_to_canyon": self.fract_heat_to_canyon,
            "shgc": self.shgc,
            "wall_albedo": self.wall_albedo,
            "roof_albedo": self.roof_albedo,
            "roof_veg_fraction": self.roof_veg_fraction
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly typology uwg parameters."""
        return 'Typology UWG Parameters: ' \
               '\n  Fraction of Heat to Canyon: {}' \
               '\n  SHGC: {}' \
               '\n  Albedo (Wall | Roof): {} | {}' \
               '\n  Roof Vegetation Fract: {}'.format(
                   self._fract_heat_to_canyon, self._shgc,
                   self._wall_albedo, self._roof_albedo,
                   self._roof_veg_fraction
               )


class TypologyDefaults(object):
    """Contains default values from the DOE commercial building reference"""

    # default wall albedos for different building types
    WALL_ALBEDO = {
        'FullServiceRestaurant': 0.15,
        'Hospital': 0.08,
        'LargeHotel': 0.08,
        'LargeOffice': 0.08,
        'MedOffice': 0.15,
        'MidRiseApartment': 0.15,
        'OutPatient': 0.15,
        'PrimarySchool': 0.15,
        'QuickServiceRestaurant': 0.22,
        'SecondarySchool': 0.15,
        'SmallHotel': 0.15,
        'SmallOffice': 0.08,
        'StandAloneRetail': 0.08,
        'StripMall': 0.08,
        'SuperMarket': 0.08,
        'WareHouse': 0.08
    }

    # default roof albedos for different construction eras
    ROOF_ALBEDO = {
        'Pre1980s': 0.2,
        '1980sPresent': 0.2,
        'NewConstruction': 0.7
    }

    # default shgcs for different climate zones and construction eras
    SHGC = {
        'Pre1980s': {
            0: 0.54,
            1: 0.54,
            2: 0.54,
            3: 0.54,
            4: 0.54,
            5: 0.54,
            6: 0.54,
            7: 0.54,
            8: 0.54,
            9: 0.54,
            10: 0.407,
            11: 0.407,
            12: 0.407,
            13: 0.407,
            14: 0.407,
        },
        '1980sPresent': {
            0: 0.251,
            1: 0.251,
            2: 0.251,
            3: 0.255,
            4: 0.44,
            5: 0.251,
            6: 0.392,
            7: 0.355,
            8: 0.362,
            9: 0.392,
            10: 0.385,
            11: 0.385,
            12: 0.385,
            13: 0.385,
            14: 0.487,
        },
        'NewConstruction': {
            0: 0.251,
            1: 0.251,
            2: 0.251,
            3: 0.252,
            4: 0.252,
            5: 0.252,
            6: 0.39,
            7: 0.385,
            8: 0.385,
            9: 0.385,
            10: 0.385,
            11: 0.385,
            12: 0.385,
            13: 0.385,
            14: 0.487,
        }
    }

    @classmethod
    def wall_albedo_by_type(cls, bldg_type):
        """Return default wall albedo based on bldg_type string."""
        return cls.WALL_ALBEDO[bldg_type]

    @classmethod
    def roof_albedo_by_era(cls, built_era):
        """Default wall albedo based on built_era string."""
        return cls.ROOF_ALBEDO[built_era]

    @classmethod
    def shgc_by_era_zone(cls, built_era, climate_zone):
        """Default solar heat coeff based on built_era string and climate_zone int."""
        return cls.SHGC[built_era][climate_zone]
