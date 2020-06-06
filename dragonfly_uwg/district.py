from __future__ import division
import math

from .dfobject import DFObject
from .bldgtypes import BuildingTypes
from .typology import Typology
from .uwg.districtpar import TrafficPar, VegetationPar, PavementPar
from .uwg.typologypar import TypologyDefaults
from .utilities import in_range


class District(DFObject):
    """Represents an urban district inclluding buildings, ground cover, and traffic.

    Properties:
        typologies
        site_area
        climate_zone
        tree_coverage_ratio
        grass_coverage_ratio
        traffic_parameters
        vegetation_parameters
        pavement_parameters
        characteristic_length
        average_bldg_height
        site_coverage_ratio
        facade_to_site_ratio
        bldg_type_ratios
    """

    def __init__(self, building_typologies, site_area, climate_zone,
                 tree_coverage_ratio=None, grass_coverage_ratio=None,
                 traffic_parameters=None, vegetation_parameters=None,
                 pavement_parameters=None, characteristic_length=None):
        """Initialize a district.

        Args:
            building_typologies: A list of dragonfly Typology objects.
            site_area: A float value representing the site area in square meters.
            climate_zone: A text string representing the ASHRAE climate zone.
                (eg. 5A). This is used to set default constructions for
                the buildings in the district.
            tree_coverage_ratio: An number from 0 to 1 that defines the
                fraction of the urban area (including both pavement
                and roofs) that is covered by trees.  The default is set to 0.
            grass_coverage_ratio: An number from 0 to 1 that defines the
                fraction of the urban area (including both pavement and roofs)
                that is covered by grass/vegetation.  The default is set to 0.
            traffic_parameters: A dragonfly TrafficPar object that defines
                the traffic within an urban area.
            vegetation_parameters: A dragonfly VegetationPar object that
                defines the behaviour of vegetation within an urban area.
            pavement_parameters: A dragonfly PavementPar object that defines
                the makeup of pavement within the urban area.
            characteristic_length: A number representing the linear dimension
                of the side of a square that encompasses the neighborhood in meters.
                The default will take the square root of the input site_area.

        Returns:
            district: The dragonfly district object
        """
        # Set the climate zone
        self._climate_zone = BuildingTypes.check_cimate_zone(climate_zone)

        # set the site_area
        assert isinstance(site_area, (float, int)), \
            'site_area must be a number. Got {}'.format(type(site_area))
        assert site_area > 0, 'site_area must be greater than 0. Got {}.'.format(
            site_area)
        self._site_area = site_area

        # set the characteristic length
        if characteristic_length is not None:
            assert isinstance(characteristic_length, (float, int)), \
                'characteristic_length must be a number got {}'.format(
                    type(characteristic_length))
            assert (characteristic_length >= 0), \
                "characteristic_length must be greater than 0"
            self._characteristic_length = characteristic_length
        else:
            self._characteristic_length = math.sqrt(self._site_area)

        # merge any typologies that are of the same DoE template.
        bldg_types = {}
        merged_types = []
        unique_count = 0
        for b_type in building_typologies:
            assert hasattr(b_type, 'isTypology'), \
                'typology is not a dragonfly typolgy object. Got {}'.format(
                    type(b_type))
            b_type_name = b_type.bldg_program + ',' + b_type.bldg_era
            if b_type_name not in bldg_types.keys():
                merged_types.append(b_type)
                bldg_types[b_type_name] = unique_count
                unique_count += 1
            else:
                type_to_merge = merged_types[bldg_types[b_type_name]]
                mergedType = Typology.create_merged_typology(b_type, type_to_merge)
                merged_types[bldg_types[b_type_name]] = mergedType

        # compute the critical geometry variables for the district
        params = self._calculate_geo_from_typologies(site_area, merged_types)
        self._average_bldg_height = params[0]
        self._site_coverage_ratio = params[1]
        self._facade_to_site_ratio = params[2]
        floor_areas, full_type_names = params[3], params[4]

        # build the dictionary of typology ratios
        total_weight = sum(floor_areas)
        typology_ratios = [x / total_weight for x in floor_areas]
        self._bldg_type_ratios = {}
        for i, key in enumerate(full_type_names):
            self._bldg_type_ratios[key] = typology_ratios[i]

        # link the typologies to the district object
        for b_typ in merged_types:
            b_typ._has_parent_district = True
            b_typ._parent_district = self
            if b_typ.uwg_parameters.shgc is None:
                b_typ._uwg_parameters._shgc = TypologyDefaults.shgc_by_era_zone(
                    b_typ.bldg_era, self._climate_zone)
        self._building_typologies = merged_types

        # set vegetation coverage
        self.tree_coverage_ratio = tree_coverage_ratio
        self.grass_coverage_ratio = grass_coverage_ratio

        # uwg parameter objects that define district conditions and are set-able.
        self.traffic_parameters = traffic_parameters
        self.vegetation_parameters = vegetation_parameters
        self.pavement_parameters = pavement_parameters

    @classmethod
    def from_json(cls, data):
        """Create a district object from a dictionary
        Args:
            data: {
                building_typologies: list of Typology objects.
                site_area: float in square meters
                climate_zone: string
                tree_coverage_ratio: float between 0 and 1
                grass_coverage_ratio: float between 0 and 1
                traffic_parameters: traffic parameter dict
                vegetation_parameters: vegetation parameter dict
                pavement_parameters: pavement parameter dict
                characteristic_length: float
            }
        """

        required_keys = ('building_typologies', 'site_area',
                         'climate_zone'
                         )
        nullable_keys = ('tree_coverage_ratio', 'grass_coverage_ratio',
                         'traffic_parameters', 'vegetation_parameters',
                         'pavement_parameters', 'characteristic_length'
                         )

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(building_typologies=[Typology.from_json(t)
                                        for t in data['building_typologies']],
                   site_area=data['site_area'],
                   climate_zone=data['climate_zone'],
                   tree_coverage_ratio=data['tree_coverage_ratio'],
                   grass_coverage_ratio=data['grass_coverage_ratio'],
                   traffic_parameters=TrafficPar.from_json(
                       data['traffic_parameters']),
                   vegetation_parameters=VegetationPar.from_json(
                       data['vegetation_parameters']),
                   pavement_parameters=PavementPar.from_json(
                       data['pavement_parameters']),
                   characteristic_length=data['characteristic_length']
                   )

    @classmethod
    def from_geo_params(cls, average_bldg_height, site_coverage_ratio,
                        facade_to_site_ratio, bldg_type_ratios, climate_zone,
                        tree_coverage_ratio=None, grass_coverage_ratio=None,
                        traffic_parameters=None, vegetation_parameters=None,
                        pavement_parameters=None, characteristic_length=None):
        """Initialize a District from a list of urban geometry parameters.

        Args:
            average_bldg_height: The average height of the buildings in meters.
            site_coverage_ratio: A number between 0 and 1 that represents the
                fraction of the district terrain that the building footprints
                occupy.  It describes how close the buildings are to one
                another in the district.
            facade_to_site_ratio: A number that represents the ratio of vertical
                urban surface area [walls] to the total terrain area of the district.
                This value can be greater than 1.
            bldg_type_ratios: A dictoinary with keys that represent the DoE
                commercial template building programs and building ages
                separated by a comma (eg. MidRiseApartment,1980sPresent).
                Under each key of the dictionary, there should be a single
                decimal number indicative of the fraction of the urban area's
                floor area taken by the typology. The sum of all decimals
                in the dictionary should equal 1.
            climate_zone: A text string representing the ASHRAE climate zone.
                (eg. 5A). This is used to set default constructions for
                the buildings in the district.
            tree_coverage_ratio: An number from 0 to 1 that defines the
                fraction of the urban area (including both pavement
                and roofs) that is covered by trees.  The default is set to 0.
            grass_coverage_ratio: An number from 0 to 1 that defines the
                fraction of the urban area (including both pavement and roofs)
                that is covered by grass/vegetation.  The default is set to 0.
            traffic_parameters: A dragonfly TrafficPar object that defines
                the traffic within an urban area.
            vegetation_parameters: A dragonfly VegetationPar object that
                defines the behaviour of vegetation within an urban area.
            pavement_parameters: A dragonfly PavementPar object that defines
                the makeup of pavement within the urban area.
            characteristic_length: A number representing the linear dimension
                of the side of a square that encompasses the neighborhood in meters.
                The default is set to 500 m, which was found to be the recomendation
                for a typical mid-density urban area.
                Street, Michael A. (2013). Comparison of simplified models of urban
                climate for improved prediction of building energy use in cities.
                Thesis (S.M. in Building Technology)--Massachusetts Institute of
                Technology, Dept. of Architecture, http://hdl.handle.net/1721.1/82284
        """

        # check geometry parameters that all districts must have and are not set-able.
        assert isinstance(average_bldg_height, (float, int)), \
            'average_bldg_height must be a number. Got {}'.format(
                type(average_bldg_height))
        assert (average_bldg_height >= 0), \
            "average_bldg_height must be greater than 0"

        assert isinstance(site_coverage_ratio, (float, int)), \
            'site_coverage_ratio must be a number. Got {}'.format(
                type(site_coverage_ratio))
        in_range(site_coverage_ratio, 0, 1, 'site_coverage_ratio')

        assert isinstance(facade_to_site_ratio, (float, int)), \
            'facade_to_site_ratio must be a number. Got {}'.format(
                type(facade_to_site_ratio))
        assert (facade_to_site_ratio >= 0), \
            "facade_to_site_ratio must be greater than 0"

        if characteristic_length is not None:
            assert isinstance(characteristic_length, (float, int)), \
                'characteristic_length must be a number got {}'.format(
                    type(characteristic_length))
            assert (characteristic_length >= 0), \
                "characteristic_length must be greater than 0"
        else:
            characteristic_length = 500.0

        # check the dictionary of building type ratios
        assert isinstance(bldg_type_ratios, dict), \
            'bldg_type_ratios must be a dictionary. Got {}'.format(
                type(facade_to_site_ratio))
        totalRatios = 0
        for typ in bldg_type_ratios.keys():
            assert isinstance(typ, str), \
                'building_type must be a string got {}'.format(
                    type(typ))
            assert isinstance(bldg_type_ratios[typ], (float, int)), \
                'building_type_ratio must be a number got {}'.format(
                    type(bldg_type_ratios[typ]))
            totalRatios += bldg_type_ratios[typ]
            try:
                bldg_program, bldg_era = typ.split(',')
                bldg_program = BuildingTypes.check_program(bldg_program)
                bldg_era = BuildingTypes.check_era(bldg_era)
            except Exception:
                raise Exception(
                    'building_type "{}" is not in the correct format'
                    ' of BldgProgram,BldgEra.'.format(typ)
                )
        assert (totalRatios == 1), \
            "Total building ratios do not sum to 1. Got {}".format(totalRatios)

        # create typology objects from the dictionary of building type ratios.
        site_area = characteristic_length**2
        _building_typologies = []
        for b_type in bldg_type_ratios.keys():
            bldg_program, bldg_era = b_type.split(',')
            district_fract = bldg_type_ratios[b_type]
            footprint_area = site_area * site_coverage_ratio * district_fract
            facade_area = site_area * facade_to_site_ratio * district_fract
            new_type = Typology(
                average_bldg_height, footprint_area, facade_area,
                bldg_program, bldg_era)
            _building_typologies.append(new_type)

        return cls(_building_typologies, site_area, climate_zone,
                   tree_coverage_ratio, grass_coverage_ratio,
                   traffic_parameters, vegetation_parameters,
                   pavement_parameters, characteristic_length)

    @property
    def building_typologies(self):
        """Return a list of building typology objects for the urban area."""
        return self._building_typologies

    @property
    def average_bldg_height(self):
        """Return the average height of the buildings in the district."""
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
        """Return the caracteristic length of the district."""
        return self._characteristic_length

    @property
    def bldg_type_ratios(self):
        """Get or set the building types and corresponding ratios as a dictionary.

        Note that setting the typology ratios here completely overwrites the
        building_typologies currently associated with this district object.
        """
        return self._bldg_type_ratios

    @property
    def bldg_types(self):
        """Return a list of the building types in the district."""
        return self._bldg_type_ratios.keys()

    @property
    def climate_zone(self):
        """Get the ASHRAE climate zone, whisch sets building constructions."""
        return BuildingTypes.get_readable_zone(self._climate_zone)

    @property
    def site_area(self):
        """Get or set the site area of the district."""
        return self._site_area

    @property
    def traffic_parameters(self):
        """Get or set the traffic parameter of the district's traffic."""
        return self._traffic_parameters

    @traffic_parameters.setter
    def traffic_parameters(self, p):
        if p is not None:
            assert hasattr(p, 'isTrafficPar'), \
                'traffic_parameters is not a dragonfly traffic_parameters' \
                ' object. Got {}'.format(type(p))
            self._traffic_parameters = p
        else:
            if self.average_bldg_height <= 10:
                p = 4.0
            elif self.average_bldg_height <= 25:
                p = 8.0
            else:
                p = 10.0
            self._traffic_parameters = TrafficPar(p)

    @property
    def vegetation_parameters(self):
        """Get or set the vegetation parameters of the district's vegetation."""
        return self._vegetation_parameters

    @vegetation_parameters.setter
    def vegetation_parameters(self, p):
        if p is not None:
            assert hasattr(p, 'isVegetationPar'), \
                'vegetation_parameters is not a dragonfly vegetation_parameters' \
                ' object. Got {}'.format(type(p))
            self._vegetation_parameters = p
        else:
            self._vegetation_parameters = VegetationPar()

    @property
    def pavement_parameters(self):
        """Get or set the pavement parameters of the district's pavement."""
        return self._pavement_parameters

    @pavement_parameters.setter
    def pavement_parameters(self, p):
        if p is not None:
            assert hasattr(p, 'isPavementPar'), \
                'pavement_parameters is not a dragonfly pavement_parameters' \
                ' object. Got {}'.format(type(p))
            self._pavement_parameters = p
        else:
            self._pavement_parameters = PavementPar()

    @property
    def tree_coverage_ratio(self):
        """Get or set the fraction of the site area covered in trees."""
        return self._tree_coverage_ratio

    @tree_coverage_ratio.setter
    def tree_coverage_ratio(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'tree_coverage_ratio must be a number got {}'.format(type(x))
            self._tree_coverage_ratio = in_range(x, 0, 1, 'tree_coverage_ratio')
        else:
            self._tree_coverage_ratio = 0

    @property
    def grass_coverage_ratio(self):
        """Get or set the fraction of the site area covered in grass."""
        return self._grass_coverage_ratio

    @grass_coverage_ratio.setter
    def grass_coverage_ratio(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'grass_coverage_ratio must be a number got {}'.format(type(x))
            self._grass_coverage_ratio = in_range(x, 0, 1, 'grass_coverage_ratio')
        else:
            self._grass_coverage_ratio = 0

    @property
    def floor_height(self):
        """Get the average floor height of the buildings in the typology."""
        weighted_sum = 0
        total_floor_area = 0
        for bldg_typ in self.building_typologies:
            weighted_sum += bldg_typ.floor_to_floor * bldg_typ.floor_area
            total_floor_area += bldg_typ.floor_area
        return weighted_sum / total_floor_area

    @property
    def glz_ratio(self):
        """Return the average glazing ratio of the buildings in the district."""
        weighted_sum = 0
        total_facade_area = 0
        for bldg_typ in self.building_typologies:
            weighted_sum += bldg_typ.glz_ratio * bldg_typ.facade_area
            total_facade_area += bldg_typ.facade_area
        return weighted_sum / total_facade_area

    @property
    def fract_heat_to_canyon(self):
        """The fraction of the building's heat that is rejected to the urban canyon."""
        weighted_sum = 0
        total_floor_area = 0
        for bldg_typ in self.building_typologies:
            weighted_sum += bldg_typ.uwg_parameters.fract_heat_to_canyon * \
                bldg_typ.floor_area
            total_floor_area += bldg_typ.floor_area
        return weighted_sum / total_floor_area

    @property
    def shgc(self):
        """Get the solar heat gain coefficient of the district's buildings."""
        weighted_sum = 0
        total_glass_area = 0
        for bldg_typ in self.building_typologies:
            if bldg_typ.uwg_parameters.shgc is None:
                bldg_typ.uwg_parameters._shgc = TypologyDefaults.shgc_by_era_zone(
                    bldg_typ.bldg_era, self._climate_zone)
            weighted_sum += bldg_typ.uwg_parameters.shgc * \
                bldg_typ.facade_area * bldg_typ.glz_ratio
            total_glass_area += (bldg_typ.facade_area * bldg_typ.glz_ratio)
        return weighted_sum / total_glass_area

    @property
    def wall_albedo(self):
        """Return the average wall albedo of the district's buildings."""
        weighted_sum = 0
        total_facade_area = 0
        for bldg_typ in self.building_typologies:
            weighted_sum += bldg_typ.uwg_parameters.wall_albedo * \
                bldg_typ.facade_area
            total_facade_area += bldg_typ.facade_area
        return weighted_sum / total_facade_area

    @property
    def roof_albedo(self):
        """Return the average roof albedo of the district's buildings."""
        weighted_sum = 0
        total_roof_area = 0
        for bldg_type in self.building_typologies:
            weighted_sum += bldg_type.uwg_parameters.roof_albedo * \
                bldg_type.footprint_area
            total_roof_area += bldg_type.footprint_area
        return weighted_sum / total_roof_area

    @property
    def roof_veg_fraction(self):
        """Return the average roof vegetated fraction of the district's buildings."""
        weighted_sum = 0
        total_roof_area = 0
        for bldg_type in self.building_typologies:
            weighted_sum += bldg_type.uwg_parameters.roof_veg_fraction * \
                bldg_type.footprint_area
            total_roof_area += bldg_type.footprint_area
        return weighted_sum / total_roof_area

    @property
    def isDistrict(self):
        """Return True for District."""
        return True

    def get_uwg_matrix(self):
        """Return a matrix of bldg programs and construction eras needed by the uwg."""
        b_type_mtx = [[0 for x in range(3)] for y in range(16)]
        for typ in self.bldg_type_ratios.keys():
            fraction = round(self.bldg_type_ratios[typ], 3)
            bldg_program, bldg_era = typ.split(',')
            program_i = BuildingTypes.get_program_index(bldg_program)
            age_i = BuildingTypes.get_era_index(bldg_era)
            b_type_mtx[program_i][age_i] = fraction
        return b_type_mtx

    @staticmethod
    def _calculate_geo_from_typologies(site_area, building_typologies):
        """Calculate district geometry parameters from site area and typologies"""
        total_footprint_area = 0
        weighted_height_sum = 0
        total_facade_area = 0
        floor_areas = []
        full_type_names = []
        for b_type in building_typologies:
            total_footprint_area += b_type.footprint_area
            weighted_height_sum += b_type.average_height * b_type.footprint_area
            total_facade_area += b_type.facade_area
            floor_areas.append(b_type.floor_area)
            full_type_names.append('{},{}'.format(b_type.bldg_program, b_type.bldg_era))
        average_bldg_height = weighted_height_sum / total_footprint_area
        site_coverage_ratio = total_footprint_area / site_area
        facade_to_site_ratio = total_facade_area / site_area

        return average_bldg_height, site_coverage_ratio, \
            facade_to_site_ratio, floor_areas, full_type_names

    def _update_geo_from_typologies(self):
        """Update district geometry parameters when an individual typology is changed."""
        # calculate geometry parameters
        params = self._calculate_geo_from_typologies(
            self.characteristic_length**2, self.building_typologies)
        self._average_bldg_height = params[0]
        self._site_coverage_ratio = params[1]
        self._facade_to_site_ratio = params[2]
        floor_areas, full_type_names = params[3], params[4]

        # update the dictionary of typology ratios
        total_weight = sum(floor_areas)
        typology_ratios = [x / total_weight for x in floor_areas]
        self._building_typologies = {}
        for i, key in enumerate(full_type_names):
            self._building_typologies[key] = typology_ratios[i]

    def to_json(self):
        """Create a district dictionary
        Results:
            {
                building_typologies: list of Typology objects.
                site_area: float in square meters
                climate_zone: string
                tree_coverage_ratio: float between 0 and 1
                grass_coverage_ratio: float between 0 and 1
                traffic_parameters: traffic parameter dict
                vegetation_parameters: vegetation parameter dict
                pavement_parameters: pavement parameter dict
                characteristic_length: float
            }
        """
        return {
            'building_typologies': [typ.to_json() for typ in self.building_typologies],
            'site_area': self.site_area,
            'climate_zone': self.climate_zone,
            'tree_coverage_ratio': self.tree_coverage_ratio,
            'grass_coverage_ratio': self.grass_coverage_ratio,
            'traffic_parameters': self.traffic_parameters.to_json(),
            'vegetation_parameters': self.vegetation_parameters.to_json(),
            'pavement_parameters': self.pavement_parameters.to_json(),
            'characteristic_length': self.characteristic_length
            }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly district."""
        typol_list = ['{} - {}'.format(
            round(self.bldg_type_ratios[x], 2), x) for x in self.bldg_types]
        typol_str = '\n     '.join(typol_list)
        return 'District: ' \
               '\n  Average Bldg Height: {} m' \
               '\n  Site Coverage Ratio: {}' \
               '\n  Facade-to-Site Ratio: {}' \
               '\n  Tree Coverage Ratio: {}' \
               '\n  Grass Coverage Ratio: {}' \
               '\n  ------------------------' \
               '\n  Building Typologies:\n     {}'.format(
                   int(self._average_bldg_height),
                   round(self._site_coverage_ratio, 2),
                   round(self._facade_to_site_ratio, 2),
                   round(self._tree_coverage_ratio, 2),
                   round(self._grass_coverage_ratio, 2),
                   typol_str
               )
