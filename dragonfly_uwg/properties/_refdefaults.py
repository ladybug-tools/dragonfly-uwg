# coding=utf-8


class _RefDefaults(object):
    """Contains default Building values from the DOE commercial building reference"""

    # default wall albedos for different building types
    WALL_ALBEDO = {
        'FullServiceRestaurant': 0.15,
        'Hospital': 0.08,
        'LargeHotel': 0.08,
        'LargeOffice': 0.08,
        'MediumOffice': 0.15,
        'MidriseApartment': 0.15,
        'Outpatient': 0.15,
        'PrimarySchool': 0.15,
        'QuickServiceRestaurant': 0.22,
        'SecondarySchool': 0.15,
        'SmallHotel': 0.15,
        'SmallOffice': 0.08,
        'Retail': 0.08,
        'StripMall': 0.08,
        'SuperMarket': 0.08,
        'Warehouse': 0.08
    }

    # default roof albedos for different construction eras
    ROOF_ALBEDO = {
        'Pre1980': 0.2,
        '1980_Present': 0.2,
        'New': 0.7
    }

    # default shgc for different climate zones and construction eras
    SHGC = {
        'Pre1980': {
            '1A': 0.54,
            '2A': 0.54,
            '2B': 0.54,
            '3A': 0.54,
            '3B': 0.54,
            '3C': 0.54,
            '4A': 0.54,
            '4B': 0.54,
            '4C': 0.54,
            '5A': 0.54,
            '5B': 0.407,
            '6A': 0.407,
            '6B': 0.407,
            '7': 0.407,
            '8': 0.407
        },
        '1980_Present': {
            '1A': 0.251,
            '2A': 0.251,
            '2B': 0.251,
            '3A': 0.255,
            '3B': 0.44,
            '3C': 0.251,
            '4A': 0.392,
            '4B': 0.355,
            '4C': 0.362,
            '5A': 0.392,
            '5B': 0.385,
            '6A': 0.385,
            '6B': 0.385,
            '7': 0.385,
            '8': 0.487
        },
        'New': {
            '1A': 0.251,
            '2A': 0.251,
            '2B': 0.251,
            '3A': 0.252,
            '3B': 0.252,
            '3C': 0.252,
            '4A': 0.39,
            '4B': 0.385,
            '4C': 0.385,
            '5A': 0.385,
            '5B': 0.385,
            '6A': 0.385,
            '6B': 0.385,
            '7': 0.385,
            '8': 0.487
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
        """Default solar heat coefficient based on built_era string and climate_zone."""
        return cls.SHGC[built_era][climate_zone]
