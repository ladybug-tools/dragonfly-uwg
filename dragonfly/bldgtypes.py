# coding=utf-8
import pickle
import os


class BuildingTypes(object):

    def __init__(self, readDOE_file_path=None):
        """Contains all of the accepted building typologies and contruction years"""

        # load  all of the building characteristcs from the pickle file.
        if readDOE_file_path is None:
            curr_dir = os.path.abspath(os.path.dirname(__file__))
            readDOE_file_path = os.path.join(curr_dir, 'resources/readDOE.pkl')
        if not os.path.exists(readDOE_file_path):
            raise Exception("readDOE.pkl file: '{}' does not exist.".format(
                readDOE_file_path))
        readDOE_file = open(readDOE_file_path, 'rb')  # open pickle file in binary form
        self.refDOE = pickle.load(readDOE_file)
        self.refBEM = pickle.load(readDOE_file)
        readDOE_file.close()

        # dictionary to go from building programs to numbers understood by the UWG
        self.bldgtype = {
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
            'Warehouse': 15
            }

        # dictionary to go from construction era to numbers understood by the UWG
        self.builtera = {
            'Pre1980s': 0,
            '1980sPresent': 1,
            'NewConstruction': 2
            }

        # dictionary to go from climate zone numbers of the UWG to human-readable format
        self.zonetype = {
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
        self.zoneconverter = {
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

        # dictionary to go from UWG building type to Dragonfly convention
        self.uwg_bldg_type = {
            'FullServiceRestaurant': 'FullServiceRestaurant',
            'Hospital': 'Hospital',
            'LargeHotel': 'LargeHotel',
            'LargeOffice': 'LargeOffice',
            'MedOffice': 'MedOffice',
            'MidRiseApartment': 'MidRiseApartment',
            'OutPatient': 'OutPatient',
            'PrimarySchool': 'PrimarySchool',
            'QuickServiceRestaurant': 'QuickServiceRestaurant',
            'SecondarySchool': 'SecondarySchool',
            'SmallHotel': 'SmallHotel',
            'SmallOffice': 'SmallOffice',
            'StandAloneRetail': 'StandAloneRetail',
            'StripMall': 'StripMall',
            'SuperMarket': 'SuperMarket',
            'WareHouse': 'Warehouse'
            }

        # dictionary to go from UWG construction era to Dragonfly convention
        self.uwg_built_era = {
            'Pre80': 'Pre1980s',
            'Pst80': '1980sPresent',
            'New': 'NewConstruction'
            }

        # dictionary of acceptable building program inputs
        self.programsDict = {
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
            'WAREHOUSE': 'Warehouse',

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
        self.ageDict = {
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

    def check_program(self, bldg_program):
        assert isinstance(bldg_program, str), \
            'bldg_program must be a text string got {}'.format(type(bldg_program))
        assert bldg_program.upper() in self.programsDict.keys(), \
            "bldg_program {} is not recognized as a valid program.".format(
                '"' + bldg_program + '"')
        return self.programsDict[str(bldg_program).upper()]

    def check_age(self, bldg_age):
        assert isinstance(bldg_age, str), \
            'bldg_age must be a text string got {}'.format(type(bldg_age))
        assert bldg_age.upper() in self.ageDict.keys(), \
            "bldg_age {} is not recognized as a valid building age.".format(
                '"' + bldg_age + '"')
        return self.ageDict[str(bldg_age).upper()]

    def check_cimate_zone(self, climate_zone):
        assert isinstance(climate_zone, str), \
            'climate_zone must be a text string got {}'.format(type(climate_zone))
        assert climate_zone.upper() in self.zoneconverter.keys(), \
            'climate_zone {} is not recognized as a valid climate zone'.format(
                climate_zone)
        return self.zoneconverter[climate_zone.upper()]
