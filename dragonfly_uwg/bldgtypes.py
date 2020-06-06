# coding=utf-8
import sys


class BuildingTypes(object):
    """Contains the accepted building typologies and contruction eras."""

    # dictionary to go from building programs to numbers understood by the UWG
    BLDG_PROGRAM = {
        'FullServiceRestaurant': 0,
        'Hospital': 1,
        'LargeHotel': 2,
        'LargeOffice': 3,
        'MedOffice': 4,
        'MidRiseApartment': 5,
        'OutPatient': 6,
        'PrimarySchool': 7,
        'QuickServiceRestaurant': 8,
        'SecondarySchool': 9,
        'SmallHotel': 10,
        'SmallOffice': 11,
        'StandAloneRetail': 12,
        'StripMall': 13,
        'SuperMarket': 14,
        'WareHouse': 15
        }

    # dictionary to get default glazing ratio depending on building program
    # values come from analysis of the DOE commercial building refernece
    GLZ_RATIO = {
        'FullServiceRestaurant': 0.182,
        'Hospital': 0.1461,
        'LargeHotel': 0.2663,
        'LargeOffice': 0.38,
        'MedOffice': 0.33,
        'MidRiseApartment': 0.1499,
        'OutPatient': 0.1985,
        'PrimarySchool': 0.35,
        'QuickServiceRestaurant': 0.14,
        'SecondarySchool': 0.34,
        'SmallHotel': 0.1087,
        'SmallOffice': 0.212,
        'StandAloneRetail': 0.071,
        'StripMall': 0.105,
        'SuperMarket': 0.109,
        'WareHouse': 0.0058
    }

    # dictionary to go from construction era to numbers understood by the UWG
    BUILT_ERA = {
        'Pre1980s': 0,
        '1980sPresent': 1,
        'NewConstruction': 2
        }

    # dictionary to go from UWG construction era to Dragonfly convention
    UWG_BUILT_ERA = {
        'Pre80': 'Pre1980s',
        'Pst80': '1980sPresent',
        'New': 'NewConstruction'
        }

    # dictionary to go from climate zone numbers of the UWG to human-readable format
    ZONE_TYPE = {
        0: '1A',
        1: '2A',
        2: '2B',
        3: '3A',
        4: '3B-CA',
        5: '3B',
        6: '3C',
        7: '4A',
        8: '4B',
        9: '4C',
        10: '5A',
        11: '5B',
        12: '6A',
        13: '6B',
        14: '7',
        15: '8'
        }

    # dictionary of acceptable ASHRAE climate zone inputs
    ZONE_CONVERTER = {
        '1A': 0,
        '2A': 1,
        '2B': 2,
        '3A': 3,
        '3B-CA': 4,
        '3B': 5,
        '3C': 6,
        '4A': 7,
        '4B': 8,
        '4C': 9,
        '5A': 10,
        '5B': 11,
        '6A': 12,
        '6B': 13,
        '7': 14,
        '8': 15,

        '1': 0,
        '2': 1,
        '3': 3,
        '4': 7,
        '5': 10,
        '6': 12,

        '1B': 0,
        '1C': 0,
        '2C': 1,
        '5C': 10,
        '6C': 12,
        '7A': 14,
        '7B': 14,
        '7C': 14,
        '8A': 15,
        '8B': 15,
        '8C': 15
    }

    # dictionary of acceptable building program inputs
    BLDG_PROGRAM_CONVERTER = {
        'FULLSERVICERESTAURANT': 'FullServiceRestaurant',
        'HOSPITAL': 'Hospital',
        'LARGEHOTEL': 'LargeHotel',
        'LARGEOFFICE': 'LargeOffice',
        'MEDIUMOFFICE': 'MediumOffice',
        'MIDRISEAPARTMENT': 'MidRiseApartment',
        'OUTPATIENT': 'OutPatient',
        'PRIMARYSCHOOL': 'PrimarySchool',
        'QUICKSERVICERESTAURANT': 'QuickServiceRestaurant',
        'SECONDARYSCHOOL': 'SecondarySchool',
        'SMALLHOTEL': 'SmallHotel',
        'SMALLOFFICE': 'SmallOffice',
        'STANDALONERETAIL': 'StandAloneRetail',
        'STRIPMALL': 'StripMall',
        'SUPERMARKET': 'SuperMarket',
        'WAREHOUSE': 'WareHouse',

        'FULL SERVICE RESTAURANT': 'FullServiceRestaurant',
        'LARGE HOTEL': 'LargeHotel',
        'LARGE OFFICE': 'LargeOffice',
        'MEDIUM OFFICE': 'MediumOffice',
        'MIDRISE APARTMENT': 'MidRiseApartment',
        'OUT PATIENT': 'OutPatient',
        'PRIMARY SCHOOL': 'PrimarySchool',
        'QUICK SERVICE RESTAURANT': 'QuickServiceRestaurant',
        'SECONDARY SCHOOL': 'SecondarySchool',
        'SMALL HOTEL': 'SmallHotel',
        'SMALL OFFICE': 'SmallOffice',
        'STANDALONE RETAIL': 'StandAloneRetail',
        'STRIP MALL': 'StripMall',

        '0': 'LargeOffice',
        '1': 'StandAloneRetail',
        '2': 'MidRiseApartment',
        '3': 'PrimarySchool',
        '4': 'SecondarySchool',
        '5': 'SmallHotel',
        '6': 'LargeHotel',
        '7': 'Hospital',
        '8': 'OutPatient',
        '9': 'Warehouse',
        '10': 'SuperMarket',
        '11': 'FullServiceRestaurant',
        '12': 'QuickServiceRestaurant',

        'Office': 'LargeOffice',
        'Retail': 'StandAloneRetail'
    }

    # dictionary of acceptable building ages
    BUILT_ERA_CONVERTER = {
        'PRE1980S': 'Pre1980s',
        '1980SPRESENT': '1980sPresent',
        'NEWCONSTRUCTION': 'NewConstruction',

        '0': 'Pre1980s',
        '1': '1980sPresent',
        '2': 'NewConstruction',

        "Pre-1980's": 'Pre1980s',
        "1980's-Present": '1980sPresent',
        'New Construction': 'NewConstruction'
    }

    @classmethod
    def check_program(cls, bldg_program):
        assert isinstance(bldg_program, str), \
            'bldg_program must be a text string. Got {}'.format(type(bldg_program))
        assert bldg_program.upper() in cls.BLDG_PROGRAM_CONVERTER.keys(), \
            'bldg_program "{}"" is not recognized as a valid program.'.format(
                bldg_program)
        return cls.BLDG_PROGRAM_CONVERTER[bldg_program.upper()]

    @classmethod
    def check_era(cls, bldg_era):
        assert isinstance(bldg_era, str), \
            'bldg_era must be a text string got {}'.format(type(bldg_era))
        assert bldg_era.upper() in cls.BUILT_ERA_CONVERTER.keys(), \
            'bldg_age "{}" is not recognized as a valid building age.'.format(
                bldg_era)
        return cls.BUILT_ERA_CONVERTER[str(bldg_era).upper()]

    @classmethod
    def check_cimate_zone(cls, climate_zone):
        assert isinstance(climate_zone, str), \
            'climate_zone must be a text string got {}'.format(type(climate_zone))
        assert climate_zone.upper() in cls.ZONE_CONVERTER.keys(), \
            'climate_zone "{}"" is not recognized as a valid climate zone'.format(
                climate_zone)
        return cls.ZONE_CONVERTER[climate_zone.upper()]

    @classmethod
    def get_program_index(cls, program):
        return cls.BLDG_PROGRAM[program]

    @classmethod
    def get_era_index(cls, era):
        return cls.BUILT_ERA[era]

    @classmethod
    def get_uwg_era_index(cls, era):
        return cls.UWG_BUILT_ERA[era]

    @classmethod
    def get_readable_zone(cls, climate_zone):
        return cls.ZONE_TYPE[climate_zone]

    @classmethod
    def default_glazing_ratio(cls, bldg_program):
        return cls.GLZ_RATIO[bldg_program]

    @classmethod
    def get_program_list(cls):
        dict = cls.BLDG_PROGRAM
        keys, vals = [], []
        if (sys.version_info < (3, 0)):
            for key, value in dict.iteritems():
                keys.append(key)
                vals.append(value)
        else:
            for key, value in dict.items():
                keys.append(key)
                vals.append(value)
        return [x for _, x in sorted(zip(vals, keys))]

    def __repr__(self):
        """BuildingTypes representation."""
        _programs = '\n  '.join(self.BLDG_PROGRAM.keys())
        _cnstr_eras = '\n  '.join(self.BUILT_ERA.keys())
        return 'Building Programs:\n  {} \n\n Construction Eras:\n  {}'.format(
            _programs, _cnstr_eras)
