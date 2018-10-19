# coding=utf-8
from __future__ import division

from dfobject import DfObject
from bldgtypes import BuildingTypes
from utilities import Utilities
import dragonfly
try:
    import plus
except ImportError as e:
    if dragonfly.isplus:
        raise ImportError(e)

bldg_types = BuildingTypes()
utilities = Utilities()


class Typology(DfObject):
    """Represents a group of buildings of the same typology in an urban area.

    Properties:
        average_height: The average height of the buildings of this typology
            in meters.
        footprint_area: The footprint area of the buildings of this typolog
            in square meteres.
        facade_area: The facade area of the buildings of this typology
            in square meters.
        bldg_program: A text string representing one of the 16 DOE building
            program types to be used as a template for this typology.
            Choose from the following options:
                FullServiceRestaurant
                Hospital
                LargeHotel
                LargeOffice
                MediumOffice
                MidRiseApartment
                OutPatient
                PrimarySchool
                QuickServiceRestaurant
                SecondarySchool
                SmallHotel
                SmallOffice
                StandAloneRetail
                StripMall
                SuperMarket
                Warehouse
        bldg_age: A text string that sets the age of the buildings represented
            by this typology. This is used to determine what constructions
            make up the walls, roofs, and windows based on international
            building codes over the last several decades.  Choose from
            the following options:
                Pre1980s
                1980sPresent
                NewConstruction
        floor_to_floor: A number that represents the average distance between
            floors for the building typology.  The default is set to 3.05 meters.
        fract_heat_to_canyon: A number from 0 to 1 that represents the fraction
            the building's waste heat from air conditioning that gets rejected
            into the urban canyon. The default is set to 0.5.
        glz_ratio: An optional number from 0 to 1 that represents the fraction
            of the walls of the building typology that are glazed. If no value
            is input here, a default will be used that comes from the DoE building
            template from the bldg_program and bldg_age.
        floor_area: A number that represents the floor area of the buiding in
            square meteres. The default is auto-calculated using the
            footprint_area, average_height, and floor_to_floor.
        number_of_stories: An integer that represents the average number of
            stories for the building typology.
    """

    def __init__(self, average_height, footprint_area, facade_area,
                 bldg_program, bldg_age, floor_to_floor=None,
                 fract_heat_to_canyon=None, glz_ratio=None, floor_area=None):
        """Initialize a dragonfly building typology"""
        # attribute to tract whether we need to update the geometry of the parent city.
        self._has_parent_city = False
        self._parent_city = None

        # critical geometry parameters that all typologies must have.
        self.average_height = average_height
        self.footprint_area = footprint_area
        self.facade_area = facade_area
        self.floor_to_floor = floor_to_floor
        self.floor_area = floor_area

        # critical program parameters that all typologies must have.
        self.bldg_program = bldg_program
        self.bldg_age = bldg_age

        # optional parameters with default values set by program.
        self.fract_heat_to_canyon = fract_heat_to_canyon
        self.glz_ratio = glz_ratio
        self.shgc = None
        self.wall_albedo = None
        self.roof_albedo = None
        self.roof_veg_fraction = None

    @classmethod
    def from_geometry(cls, bldg_breps, bldg_program, bldg_age, floor_to_floor=None,
                      fract_heat_to_canyon=None, glz_ratio=None):
        """Initialize a building typology from closed building brep geometry

        Args:
            bldg_breps: A list of closed rhino breps representing
                buildings of the typology.
            bldg_program: A text string representing one of the 16 DOE building
                program types to be used as a template for this typology.
            bldg_age: A text string that sets the age of the buildings represented
                by this typology.
            floor_to_floor: A number that represents the average distance between
                floors. Default is set to 3.05 meters.
            glz_ratio: An optional number from 0 to 1 that represents the fraction
                of the walls of the building typology that are glazed. Default will
                come from the DoE building template from the bldg_program and bldg_age.
            fract_heat_to_canyon: An optional number from 0 to 1 that represents
                the fraction the building's waste heat from air conditioning that
                gets rejected into the urban canyon. The default is set to 0.5.

        Returns:
            typology: The dragonfly typology object
            footprint_breps: Breps representing the footprints of the buildings.
            floor_breps: Breps representing the floors of the buildings in the typology.
            facade_breps: Breps representing the exposed facade surfaces of the typology.
        """
        assert dragonfly.isplus, \
            '"from_geometry" method can only be used in [+] libraries.'

        avgBldgHeight, footprintArea, floorArea, facadeArea, footprint_breps, \
            floor_breps, facade_breps = plus.calculateTypologyGeoParams(
                bldg_breps, floor_to_floor)

        typology = cls(avgBldgHeight, footprintArea, facadeArea,
                       bldg_program, bldg_age, floor_to_floor,
                       fract_heat_to_canyon, glz_ratio, floorArea)

        return typology, footprint_breps, floor_breps, facade_breps

    @classmethod
    def from_footprints(cls, bldg_footprint_breps, num_stories, bldg_program,
                        bldg_age, floor_to_floor=None, fract_heat_to_canyon=None,
                        glz_ratio=None):
        """Initialize typology from building footprints and an average number of stories.

        Args:
            bldg_footprint_breps: A list of surface rhino breps representing
                the building footprints of the typology.
            num_stories: A float value (greater than or equal to 1) that represents
                the average number of stories of the buildings in the typology.
            bldg_program: A text string representing one of the 16 DOE building
                program types to be used as a template for this typology.
            bldg_age: A text string that sets the age of the buildings represented
                by this typology.
            floor_to_floor: A number that represents the average distance
                between floors. Default is set to 3.05 meters.
            glz_ratio: An optional number from 0 to 1 that represents the
                fraction of the walls of the building typology that are
                glazed. Default will come from the DoE building template from
                the bldg_program and bldg_age.
            fract_heat_to_canyon: An optional number from 0 to 1 that represents
                the fraction the building's waste heat from air conditioning
                that gets rejected into the urban canyon. The default is set to 0.5.

        Returns:
            typology: The dragonfly typology object
            perimeter_curves: The exterior-exposed curves of the footprints.
        """
        assert num_stories >= 1, \
            'num_stories must be greater than or equal to 1. Got {}'.format(
                str(num_stories))

        assert dragonfly.isplus, \
            '"from_geometry" method can only be used in [+] libraries.'

        footprint_area, perimeter_length, perimeter_curves = \
            plus.calculateFootprintGeoParams(bldg_footprint_breps)

        if floor_to_floor is not None:
            avg_bldg_height = floor_to_floor * num_stories
        else:
            avg_bldg_height = 3.05 * num_stories
        facade_area = perimeter_length * avg_bldg_height
        floor_area = footprint_area * num_stories

        typology = cls(avg_bldg_height, footprint_area, facade_area,
                       bldg_program, bldg_age, floor_to_floor,
                       fract_heat_to_canyon, glz_ratio, floor_area)

        return typology, perimeter_curves

    @classmethod
    def from_footprints_and_stories(cls, bldg_footprint_breps, num_stories,
                                    bldg_program, bldg_age, floor_to_floor=None,
                                    fract_heat_to_canyon=None, glz_ratio=None):
        """Initialize typology from building footprints and list of building stories.

        Args:
            bldg_footprint_breps: A list of surface rhino breps representing
                the building footprints of the typology.
            num_stories: A list of integer values (all greater than or equal
                to 1) that represent the number of stories for each of the
                surfaces in the bldg_footprint_breps.
            bldg_program: A text string representing one of the 16 DOE building
                program types to be used as a template for this typology.
            bldg_age: A text string that sets the age of the buildings
                represented by this typology.
            floor_to_floor: A number that represents the average distance
                between floors. Default is set to 3.05 meters.
            glz_ratio: An optional number from 0 to 1 that represents the
                fraction of the walls of the building typology that are glazed.
                Default will come from the DoE building template from the
                bldg_program and bldg_age.
            fract_heat_to_canyon: An optional number from 0 to 1 that represents
                the fraction the building's waste heat from air conditioning
                that gets rejected into the urban canyon. The default is set to 0.5.

        Returns:
            typology: The dragonfly typology object
            perimeter_curves: The exterior-exposed curves of the footprints.
        """
        assert dragonfly.isplus, \
            '"from_geometry" method can only be used in [+] libraries.'

        weighted_num_stories = 0
        total_ftp_area = 0
        for i, floor_srf in enumerate(bldg_footprint_breps):
            f_area = plus.calculate_area(floor_srf)
            weighted_num_stories += f_area * num_stories[i]
            total_ftp_area += f_area
        avg_num_stories = weighted_num_stories / total_ftp_area

        return cls.from_footprints(bldg_footprint_breps, avg_num_stories,
                                   bldg_program, bldg_age, floor_to_floor,
                                   fract_heat_to_canyon, glz_ratio)

    @classmethod
    def create_merged_typology(cls, typology_one, typology_two):
        """Creates a merged typology between two typologies of the same building type.

        Args:
            typology_one: The first Dragonfly building typology.
            typology_two: The second Dragonfly building typology.

        Returs:
            merged_typology: A Dragonfly typology representing the
                merged previous typologies.
        """
        # checks
        assert (hasattr(typology_one, 'isTypology')), \
            'typology_one must be a Dragonfly typology. got {}'.format(
                type(typology_one))
        assert (hasattr(typology_two, 'isTypology')), \
            'typology_two must be a Dragonfly typology. got {}'.format(
                type(typology_two))
        assert (typology_one.bldg_program == typology_two.bldg_program), \
            "bldg_program of one: {} does not match that of two: {}".format(
                typology_one.bldg_program, typology_two.bldg_program)
        assert (typology_one.bldg_age == typology_two.bldg_age), \
            "bldg_age of this one: {} does not match that of two: {}".format(
                typology_one.bldg_age, typology_two.bldg_age)

        # attributes that get totalled
        new_footprint_area = typology_one.footprint_area + typology_two.footprint_area
        new_facade_area = typology_one.facade_area + typology_two.facade_area
        new_floor_area = typology_one.floor_area + typology_two.floor_area

        # atributes that get weighted averaged.
        new_average_height = (typology_one.average_height *
                              typology_one.footprint_area +
                              typology_two.average_height *
                              typology_two.footprint_area) / new_footprint_area
        new_floor_to_floor = (typology_one.floor_to_floor *
                              typology_one.floor_area +
                              typology_two.floor_to_floor *
                              typology_two.floor_area)/new_floor_area
        new_fract_heat_to_canyon = (typology_one.fract_heat_to_canyon *
                                    typology_one.floor_area +
                                    typology_two.fract_heat_to_canyon *
                                    typology_two.floor_area) / new_floor_area
        new_glz_ratio = (typology_one.glz_ratio * typology_one.facade_area +
                         typology_two.glz_ratio * typology_two.facade_area
                         ) / new_facade_area
        new_wall_albedo = (typology_one.wall_albedo * typology_one.facade_area +
                           typology_two.wall_albedo * typology_two.facade_area
                           ) / new_facade_area

        newtypology = cls(new_average_height, new_footprint_area,
                          new_facade_area, typology_one.bldg_program,
                          typology_one.bldg_age, new_floor_to_floor,
                          new_fract_heat_to_canyon, new_glz_ratio, new_floor_area)
        newtypology.wall_albedo = new_wall_albedo

        return newtypology

    @property
    def average_height(self):
        """Get or set the average height of the buildings in meters."""
        return self._average_height

    @average_height.setter
    def average_height(self, h):
        assert isinstance(h, (float, int)), \
            'average_height must be a number got {}'.format(type(h))
        assert (h >= 0), "average_height must be greater than 0"
        self._average_height = h
        if self.has_parent_city is True:
            self.parent_city.update_geo_from_typologies()

    @property
    def footprint_area(self):
        """Get or set the footprint of the buildings in square meters."""
        return self._footprint_area

    @footprint_area.setter
    def footprint_area(self, a):
        assert isinstance(a, (float, int)), \
            'footprint_area must be a number got {}'.format(type(a))
        assert (a >= 0), "footprint_area must be greater than 0"
        self._footprint_area = a
        if self.has_parent_city is True:
            self.parent_city.update_geo_from_typologies()

    @property
    def facade_area(self):
        """Get or set the facade area of the buildings in square meters."""
        return self._facade_area

    @facade_area.setter
    def facade_area(self, a):
        assert isinstance(a, (float, int)), \
            'facade_area must be a number got {}'.format(type(a))
        assert (a >= 0), "facade_area must be greater than 0"
        self._facade_area = a
        if self.has_parent_city is True:
            self.parent_city.update_geo_from_typologies()

    @property
    def floor_to_floor(self):
        """Get or set the facade area of the buildings in square meters."""
        return self._floor_to_floor

    @floor_to_floor.setter
    def floor_to_floor(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'floor_to_floor must be a number got {}'.format(type(x))
            assert (x >= 0), "floor_to_floor must be greater than 0"
            self._floor_to_floor = x
        else:
            self._floor_to_floor = 3.05

    @property
    def number_of_stories(self):
        """Return the average number of stories in the buildings."""
        return int(round(self.average_height / self.floor_to_floor))

    @property
    def floor_area(self):
        """Get or set the interior floor area of the buildings in square meters."""
        return self._floor_area

    @floor_area.setter
    def floor_area(self, a):
        if a is not None:
            assert isinstance(a, (float, int)), \
                'floor_area must be a number got {}'.format(type(a))
            assert (a >= self._footprint_area), \
                "floor_area {} cannot be smaller than the footprint_area {}".format(
                str(a), str(self._footprint_area))
            self._floor_area = a
        else:
            self._floor_area = self._footprint_area * self.number_of_stories
        if self.has_parent_city is True:
            self.parent_city.update_geo_from_typologies()

    @property
    def bldg_program(self):
        """Get or set the program of the buildings in the typology."""
        return self._bldg_program

    @bldg_program.setter
    def bldg_program(self, prog):
        self._bldg_program = bldg_types.check_program(prog)

    @property
    def bldg_age(self):
        """Get or set the construction time of buildings in the typology."""
        return self._bldg_age

    @bldg_age.setter
    def bldg_age(self, age):
        self._bldg_age = bldg_types.check_age(age)

    @property
    def fract_heat_to_canyon(self):
        """Get or set the fraction of the bldg heat rejected to the urban canyon."""
        return self._fract_heat_to_canyon

    @fract_heat_to_canyon.setter
    def fract_heat_to_canyon(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'fract_heat_to_canyon must be a number got {}'.format(type(x))
            self._fract_heat_to_canyon = utilities.in_range(x, 0, 1, 'fract_heat_to_canyon')
        else:
            self._fract_heat_to_canyon = 0.5

    @property
    def glz_ratio(self):
        """Get or set the glazing ratio of the buildings in the typology."""
        return self._glz_ratio

    @glz_ratio.setter
    def glz_ratio(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'glz_ratio must be a number got {}'.format(type(x))
            self._glz_ratio = utilities.in_range(x, 0, 1, 'glz_ratio')
        else:
            self._glz_ratio = \
                float(bldg_types.refBEM[bldg_types.bldgtype[self.bldg_program]]
                      [bldg_types.builtera[self.bldg_age]][0].building.glazingRatio)

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
            self._shgc = utilities.in_range(x, 0, 1, 'shgc')

    def get_default_shgc(self, climate_zone):
        """Returns the default solar heat gain coefficient given the climate_zone."""
        zoneIndex = bldg_types.check_cimate_zone(climate_zone)
        return float(bldg_types.refBEM[bldg_types.bldgtype[self.bldg_program]]
                     [bldg_types.builtera[self.bldg_age]][zoneIndex].building.shgc)

    @property
    def wall_albedo(self):
        """Get or set the exterior wall albedo of the buildings in the typology."""
        return self._wall_albedo

    @wall_albedo.setter
    def wall_albedo(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'wall_albedo must be a number got {}'.format(type(x))
            self._wall_albedo = utilities.in_range(x, 0, 1, 'wall_albedo')
        else:
            self._wall_albedo = \
                float(bldg_types.refBEM[bldg_types.bldgtype[self.bldg_program]]
                      [bldg_types.builtera[self.bldg_age]][0].wall.albedo)

    @property
    def roof_albedo(self):
        """Get or set the exterior roof albedo of the buildings in the typology."""
        return self._roof_albedo

    @roof_albedo.setter
    def roof_albedo(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'roof_albedo must be a number got {}'.format(type(x))
            self._roof_albedo = utilities.in_range(x, 0, 1, 'roof_albedo')
        else:
            self._roof_albedo = \
                float(bldg_types.refBEM[bldg_types.bldgtype[self.bldg_program]]
                      [bldg_types.builtera[self.bldg_age]][0].roof.albedo)

    @property
    def roof_veg_fraction(self):
        """Get or set the roof vegetation fraction of the buildings in the typology."""
        return self._roof_albedo

    @roof_veg_fraction.setter
    def roof_veg_fraction(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'roof_veg_fraction must be a number got {}'.format(type(x))
            self._roof_veg_fraction = utilities.in_range(x, 0, 1, 'roof_veg_fraction')
        else:
            self._roof_veg_fraction = 0.

    @property
    def has_parent_city(self):
        return self._has_parent_city

    @property
    def parent_city(self):
        return self._parent_city

    @property
    def isTypology(self):
        """Return True for Typology."""
        return True

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly typology."""
        return 'Building Typology: ' + \
               '\n  ' + self._bldg_program + ", " + self._bldg_age + \
               '\n  Average Height: ' + str(int(self._average_height)) + " m" + \
               '\n  Number of Stories: ' + str(self.number_of_stories) + \
               '\n  Floor Area: {:,.0f}'.format(self.floor_area) + " m2" + \
               '\n  Footprint Area: {:,.0f}'.format(self.footprint_area) + " m2" + \
               '\n  Facade Area: {:,.0f}'.format(self.facade_area) + " m2" + \
               '\n  Glazing Ratio: ' + str(int(self.glz_ratio*100)) + "%"
