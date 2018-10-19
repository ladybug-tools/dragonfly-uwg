from __future__ import division

from dragonfly.dfobject import DfObject
from dragonfly.utilities import Utilities
from dragonfly.typology import Typology
from dragonfly.dfparameter import VegetationPar, PavementPar
from dragonfly.bldgtypes import BuildingTypes

import math


class City(DfObject):
    """Represents a an entire uban area inclluding buildings, pavement, vegetation, and traffic.

    Properties:
        average_bldg_height: The average height of the buildings of the city in meters.
        site_coverage_ratio: A number between 0 and 1 that represents the fraction of the city terrain
            the building footprints occupy.  It describes how close the buildings are to one another in the city.
        facade_to_site_ratio: A number that represents the ratio of vertical urban surface area [walls] to
            the total terrain area of the city.  This value can be greater than 1.
        bldg_type_ratios: A dictoinary with keys that represent the DoE template building programs and building ages
            separated by a comma (eg. MidRiseApartment,1980sPresent).  Under each key of the dictionary, there should
            be a single decimal number indicative of the fraction of the urban area's floor area taken by the typology.
            The sum of all fractions in the dictionary should equal 1. Here is an example dictionary:
        climate_zone: A text string representing the ASHRAE climate zone. (eg. 5A). This is used to set
            default constructions for the buildings in the city.
        traffic_parameters: A dragonfly TrafficPar object that defines the traffic within an urban area.
        tree_coverage_ratio: An number from 0 to 1 that defines the fraction of the entire urban area
            (including both pavement and roofs) that is covered by trees.  The default is set to 0.
        grass_coverage_ratio: An number from 0 to 1 that defines the fraction of the entire urban area
            (including both pavement and roofs) that is covered by grass/vegetation.  The default is set to 0.
        vegetation_parameters: A dragonfly VegetationPar object that defines the behaviour of vegetation within an urban area.
        pavement_parameters: A dragonfly PavementPar object that defines the makeup of pavement within the urban area.
        characteristic_length: A number representing the linear dimension of the side of a square that encompasses the neighborhood in meters.
            The default is set to 500 m, which was found to be the recomendation for a typical mid-density urban area.
            Street, Michael A. (2013). Comparison of simplified models of urban climate for improved prediction of building
            energy use in cities. Thesis (S.M. in Building Technology)--Massachusetts Institute of Technology, Dept. of Architecture,
            http://hdl.handle.net/1721.1/82284
    """

    def __init__(self, average_bldg_height, site_coverage_ratio, facade_to_site_ratio,
                bldg_type_ratios, climate_zone, traffic_parameters, tree_coverage_ratio=None,
                grass_coverage_ratio=None, vegetation_parameters=None,
                pavement_parameters=None, characteristic_length=500, readDOE_file_path=None):
        """Initialize a dragonfly city"""
        # get dependencies
        self.genChecks = Utilities()

        # set building types
        self.bldgTypes = BuildingTypes()

        # critical geometry parameters that all cities must have and are not set-able.
        assert isinstance(average_bldg_height, (float, int)), 'average_bldg_height must be a number got {}'.format(type(average_bldg_height))
        assert (average_bldg_height >= 0), "average_bldg_height must be greater than 0"
        self._average_bldg_height = average_bldg_height
        assert isinstance(site_coverage_ratio, (float, int)), 'site_coverage_ratio must be a number got {}'.format(type(site_coverage_ratio))
        self._site_coverage_ratio = self.genChecks.in_range(site_coverage_ratio, 0, 1, 'site_coverage_ratio')
        assert isinstance(facade_to_site_ratio, (float, int)), 'facade_to_site_ratio must be a number got {}'.format(type(facade_to_site_ratio))
        assert (facade_to_site_ratio >= 0), "facade_to_site_ratio must be greater than 0"
        self._facade_to_site_ratio = facade_to_site_ratio
        assert isinstance(characteristic_length, (float, int)), 'characteristic_length must be a number got {}'.format(type(characteristic_length))
        assert (characteristic_length >= 0), "characteristic_length must be greater than 0"
        self._characteristic_length = characteristic_length

        # critical program parameters that all typologies must have and are set-able.
        self._bldg_type_ratios = bldg_type_ratios
        self._building_typologies = None
        self._are_typologies_loaded = False

        # dragonfly parameter objects that define conditions within the city and are set-able.
        self.climate_zone = climate_zone
        self.traffic_parameters = traffic_parameters
        self.vegetation_parameters = vegetation_parameters
        self.pavement_parameters = pavement_parameters

        # vegetation coverage
        self.tree_coverage_ratio = tree_coverage_ratio
        self.grass_coverage_ratio = grass_coverage_ratio

    @classmethod
    def from_typologies(cls, typologies, terrain, climate_zone, traffic_parameters, tree_coverage_ratio=None,
                        grass_coverage_ratio=None, vegetation_parameters=None, pavement_parameters=None,
                        readDOE_file_path=None):
        """Initialize a city from a list of building typologies
        Args:
            typologies: A list of dragonfly Typology objects.
            terrain: A dragonfly Terrain object.
            climate_zone: A text string representing the ASHRAE climate zone. (eg. 5A). This is used to set
                default constructions for the buildings in the city.
            traffic_parameters: A dragonfly TrafficPar object that defines the traffic within an urban area.
            tree_coverage_ratio: An number from 0 to 1 that defines the fraction of the entire urban area
                (including both pavement and roofs) that is covered by trees.  The default is set to 0.
            grass_coverage_ratio: An number from 0 to 1 that defines the fraction of the entire urban area
                (including both pavement and roofs) that is covered by grass/vegetation.  The default is set to 0.
            vegetation_parameters: A dragonfly VegetationPar object that defines the behaviour of vegetation within an urban area.
            pavement_parameters: A dragonfly PavementPar object that defines the makeup of pavement within the urban area.

        Returns:
            city: The dragonfly city object
        """
        # merge any typologies that are of the same DoE template.
        bldgTypes = {}
        mergedTypes = []
        uniqueCount = 0
        for bType in typologies:
            assert hasattr(bType, 'isTypology'), 'typology is not a dragonfly typolgy object. Got {}'.format(type(bType))
            bTypeName = bType.bldg_program + ',' + bType.bldg_age
            if bTypeName not in bldgTypes.keys():
                mergedTypes.append(bType)
                bldgTypes[bTypeName] = uniqueCount
                uniqueCount += 1
            else:
                typeToMerge = mergedTypes[bldgTypes[bTypeName]]
                mergedType = Typology.create_merged_typology(bType, typeToMerge)
                mergedTypes[bldgTypes[bTypeName]] = mergedType

        # process the terrain surface.
        assert hasattr(terrain, 'isTerrain'), 'terrain is not a dragonfly terrain object. Got {}'.format(type(terrain))
        terrainArea = terrain.area

        # compute the critical geometry variables for the city
        totalFootprintArea = 0
        weightedHeightSum = 0
        totalFacadeArea = 0
        floorAreas = []
        fullTypeNames = []
        for bType in mergedTypes:
            totalFootprintArea += bType.footprint_area
            weightedHeightSum += bType.average_height*bType.footprint_area
            totalFacadeArea += bType.facade_area
            floorAreas.append(bType.floor_area)
            fullTypeNames.append(bType.bldg_program + ',' + bType.bldg_age)
        avgBldgHeight = weightedHeightSum/totalFootprintArea
        bldgCoverage = totalFootprintArea/terrainArea
        facadeToSite = totalFacadeArea/terrainArea

        # build the dictionary of typology ratios
        totalWeight = sum(floorAreas)
        typologyRatios = [x/totalWeight for x in floorAreas]
        bldgTypeDict = {}
        for i, key in enumerate(fullTypeNames):
            bldgTypeDict[key] = typologyRatios[i]

        # create the city object.
        dfCity = cls(avgBldgHeight, bldgCoverage, facadeToSite, bldgTypeDict, climate_zone,
                     traffic_parameters, tree_coverage_ratio, grass_coverage_ratio, vegetation_parameters,
                     pavement_parameters, terrain.characteristic_length,
                     readDOE_file_path=readDOE_file_path)

        # link the typologies to the city object
        for bTyp in mergedTypes:
            bTyp._has_parent_city = True
            bTyp._parent_city = dfCity
            if bTyp.shgc == None:
                bTyp.shgc = bTyp.get_default_shgc(dfCity.climate_zone)
        dfCity._building_typologies = mergedTypes
        dfCity._are_typologies_loaded = True

        return dfCity

    @property
    def average_bldg_height(self):
        """Return the average height of the buildings in the city."""
        return self._average_bldg_height

    @property
    def site_coverage_ratio(self):
        """Return the site coverage ratio of buildings to terrain."""
        return self._site_coverage_ratio

    @property
    def facade_to_site_ratio(self):
        """Return the facade to site ratio."""
        return self._facade_to_site_ratio

    @property
    def characteristic_length(self):
        """Return the caracteristic length of the city."""
        return self._characteristic_length

    @property
    def bldg_types(self):
        """Return a list of the building types in the city."""
        return self._bldg_type_ratios.keys()

    @property
    def bldg_type_ratios(self):
        """Get or set the building types and corresponding ratios as a dictionary.

        Note that setting the typology ratios here completely overwrites the
        building_typologies currently associated with this city object.
        """
        return self._bldg_type_ratios

    @bldg_type_ratios.setter
    def bldg_type_ratios(self, bldg_type_dict):
        totalRatios = 0
        for type in bldg_type_dict.keys():
            assert isinstance(type, str), 'building_type must be a string got {}'.format(type(type))
            assert isinstance(bldg_type_dict[type], (float, int)), 'building_type ratio must be a number got {}'.format(type(bldg_type_dict[type]))
            totalRatios += bldg_type_dict[type]
            try:
                bldg_program, bldg_age = type.split(',')
                bldg_program = self.bldgTypes.check_program(bldg_program)
                bldg_age = self.bldgTypes.check_age(bldg_age)
            except:
                raise Exception (
                    "Building Type {} is not in the correct format of BuildingProgram,BuildingAge.".format('"' + str(type) + '"')
                )
        assert (totalRatios == 1), "Total building ratios do not sum to 1. Got {}".format(str(totalRatios))
        self._bldg_type_ratios = bldg_type_dict
        self._are_typologies_loaded = False

    @property
    def building_typologies(self):
        """Return a list of dragonfly building typology objects for the urban area."""
        if self.are_typologies_loaded is True:
            return self._building_typologies
        else:
            # build dragonfly typology objects from the dictionary of building type ratios.
            self._building_typologies = []
            for bType in self.bldg_type_ratios.keys():
                bldg_program, bldg_age = bType.split(',')
                cityFract = self.bldg_type_ratios[bType]
                site_area = math.pow(self.characteristic_length, 2) * math.pi
                footprint_area = site_area * self.site_coverage_ratio * cityFract
                facade_area = site_area * self.facade_to_site_ratio * cityFract
                newType = Typology(self.average_bldg_height, footprint_area, facade_area, bldg_program, bldg_age)
                newType._parent_city = self
                newType._has_parent_city = True
                newType.shgc = newType.get_default_shgc(self.climate_zone)
                self._building_typologies.append(newType)
            self._are_typologies_loaded = True
            return self._building_typologies

    @property
    def climate_zone(self):
        """Get or set the ASHRAE climate zone that dictates the nature of the constructions of the buildings."""
        return self.bldgTypes.zonetype[self._climate_zone]

    @climate_zone.setter
    def climate_zone(self, z):
        assert isinstance(z, str), 'climate_zone must be a text string got {}'.format(type(z))
        assert z.upper() in self.bldgTypes.zoneconverter.keys(), 'climate_zone {} is not recognized as a valid climate zone'.format(z)
        self._climate_zone = self.bldgTypes.zoneconverter[z.upper()]

    @property
    def traffic_parameters(self):
        """Get or set the traffic parameter object that describes the city's traffic."""
        return self._traffic_parameters

    @traffic_parameters.setter
    def traffic_parameters(self, p):
        assert hasattr(p, 'isTrafficPar'), 'traffic_parameters is not a dragonfly traffic_parameters object. Got {}'.format(type(p))
        self._traffic_parameters = p

    @property
    def vegetation_parameters(self):
        """Get or set the vegetation parameter object that describes the city's vegetation."""
        return self._vegetation_parameters

    @vegetation_parameters.setter
    def vegetation_parameters(self, p):
        if p is not None:
            assert hasattr(p, 'isVegetationPar'), 'vegetation_parameters is not a dragonfly vegetation_parameters object. Got {}'.format(type(p))
            self._vegetation_parameters = p
        else:
            self._vegetation_parameters = VegetationPar()

    @property
    def pavement_parameters(self):
        """Get or set the pavement parameter object that describes the city's pavement."""
        return self._pavement_parameters

    @pavement_parameters.setter
    def pavement_parameters(self, p):
        if p is not None:
            assert hasattr(p, 'isPavementPar'), 'pavement_parameters is not a dragonfly pavement_parameters object. Got {}'.format(type(p))
            self._pavement_parameters = p
        else:
            self._pavement_parameters = PavementPar()

    @property
    def tree_coverage_ratio(self):
        """Get or set the ratio of the entire site area of the city covered in trees."""
        return self._tree_coverage_ratio

    @tree_coverage_ratio.setter
    def tree_coverage_ratio(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), 'tree_coverage_ratio must be a number got {}'.format(type(x))
            self._tree_coverage_ratio = self.genChecks.in_range(x, 0, 1, 'tree_coverage_ratio')
        else:
            self._tree_coverage_ratio = 0

    @property
    def grass_coverage_ratio(self):
        """Get or set the ratio of the entire site area of the city covered in grass."""
        return self._grass_coverage_ratio

    @grass_coverage_ratio.setter
    def grass_coverage_ratio(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), 'grass_coverage_ratio must be a number got {}'.format(type(x))
            self._grass_coverage_ratio = self.genChecks.in_range(x, 0, 1, 'grass_coverage_ratio')
        else:
            self._grass_coverage_ratio = 0

    @property
    def floor_height(self):
        """Get the average floor height of the buildings in the typology."""
        weighted_sum = 0
        totalFloorArea = 0
        for bldgType in self.building_typologies:
            weighted_sum += bldgType.floor_to_floor * bldgType.floor_area
            totalFloorArea += bldgType.floor_area
        return weighted_sum / totalFloorArea

    @property
    def fract_heat_to_canyon(self):
        """Return the fraction of the building's heat that is rejected to the urban canyon."""
        weighted_sum = 0
        totalFlrArea = 0
        for bldgType in self.building_typologies:
            weighted_sum += bldgType.fract_heat_to_canyon * bldgType.floor_area
            totalFlrArea += bldgType.floor_area
        return weighted_sum / totalFlrArea

    @property
    def glz_ratio(self):
        """Return the average glazing ratio of the buildings in the city."""
        weighted_sum = 0
        totalFacadeArea = 0
        for bldgType in self.building_typologies:
            weighted_sum += bldgType.glz_ratio*bldgType.facade_area
            totalFacadeArea += bldgType.facade_area
        return weighted_sum / totalFacadeArea

    @property
    def shgc(self):
        """Get the solar heat gain coefficient of the buildings in the typology."""
        weighted_sum = 0
        totalFacadeArea = 0
        for bldgType in self.building_typologies:
            if bldgType.shgc is None:
                bldgType.shgc = bldgType.get_default_shgc(self.climate_zone)
            weighted_sum += bldgType.shgc * bldgType.facade_area
            totalFacadeArea += bldgType.facade_area
        return weighted_sum / totalFacadeArea

    @property
    def wall_albedo(self):
        """Return the average wall albedo of the buildings in the city."""
        weighted_sum = 0
        totalFacadeArea = 0
        for bldgType in self.building_typologies:
            weighted_sum += bldgType.wall_albedo * bldgType.facade_area
            totalFacadeArea += bldgType.facade_area
        return weighted_sum / totalFacadeArea

    @property
    def roof_albedo(self):
        """Return the average roof albedo of the buildings in the city."""
        weighted_sum = 0
        total_roof_area = 0
        for bldg_type in self.building_typologies:
            weighted_sum += bldg_type.roof_albedo * bldg_type.footprint_area
            total_roof_area += bldg_type.footprint_area
        return weighted_sum / total_roof_area

    @property
    def roof_veg_fraction(self):
        """Return the average roof vegetated fraction of the buildings in the city."""
        weighted_sum = 0
        total_roof_area = 0
        for bldg_type in self.building_typologies:
            weighted_sum += bldg_type.roof_veg_fraction * bldg_type.footprint_area
            total_roof_area += bldg_type.footprint_area
        return weighted_sum / total_roof_area

    @property
    def are_typologies_loaded(self):
        """Return True when typologies need to be created or re-generated."""
        return self._are_typologies_loaded

    @property
    def isCity(self):
        """Return True for City."""
        return True

    def get_uwg_matrix(self):
        """Return a matrix of bldg typologies and construction eras that be assigned to the uwg."""
        bTypeMtx = [[0 for x in range(3)] for y in range(16)]
        for type in self.bldg_type_ratios.keys():
            fraction = round(self.bldg_type_ratios[type], 3)
            bldg_program, bldg_age = type.split(',')
            program_i = self.bldgTypes.bldgtype[bldg_program]
            age_i = self.bldgTypes.builtera[bldg_age]
            bTypeMtx[program_i][age_i] = fraction
        return bTypeMtx

    def update_geo_from_typologies(self):
        """Updates the city-wide geometry parameters whenever an individual building typology's have changed."""
        site_area = math.pow(self.characteristic_length,2) * math.pi
        totalFootprintArea = 0
        weightedHeightSum = 0
        totalFacadeArea = 0
        floorAreas = []
        fullTypeNames = []
        for bType in self.building_typologies:
            totalFootprintArea += bType.footprint_area
            weightedHeightSum += bType.average_height * bType.footprint_area
            totalFacadeArea += bType.facade_area
            floorAreas.append(bType.floor_area)
            fullTypeNames.append(bType.bldg_program + ',' + bType.bldg_age)
        self._average_bldg_height = weightedHeightSum/totalFootprintArea
        self._site_coverage_ratio = totalFootprintArea/site_area
        self._facade_to_site_ratio = totalFacadeArea/site_area

        totalWeight = sum(floorAreas)
        typologyRatios = [x/totalWeight for x in floorAreas]
        self._building_typologies = {}
        for i, key in enumerate(fullTypeNames):
            self._building_typologies[key] = typologyRatios[i]

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly city."""
        typologyList = ''
        for x in self.bldg_types:
            typologyList = typologyList + '\n     ' + str(round(self.bldg_type_ratios[x], 2)) + ' - ' + x
        return 'City: ' + \
               '\n  Average Bldg Height: ' + str(int(self._average_bldg_height)) + " m" + \
               '\n  Site Coverage Ratio: ' + str(round(self._site_coverage_ratio, 2)) + \
               '\n  Facade-to-Site Ratio: ' + str(round(self._facade_to_site_ratio, 2)) + \
               '\n  Tree Coverage Ratio: ' + str(round(self._tree_coverage_ratio, 2)) + \
               '\n  Grass Coverage Ratio: ' + str(round(self._grass_coverage_ratio, 2)) + \
               '\n  ------------------------' + \
               '\n  Building Typologies: ' + typologyList
