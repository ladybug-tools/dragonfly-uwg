# coding=utf-8
from __future__ import division
from copy import deepcopy

from .dfobject import DFObject
from .bldgtypes import BuildingTypes
from .uwg.typologypar import TypologyPar, TypologyDefaults
from .utilities import in_range

import dragonfly
try:
    import plus
except ImportError as e:
    if dragonfly.isplus:
        raise ImportError(e)


class Typology(DFObject):
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
        bldg_era: A text string that sets the age of the buildings represented
            by this typology. This is used to determine what constructions
            make up the walls, roofs, and windows based on international
            building codes over the last several decades.  Choose from
            the following options:
                Pre1980s
                1980sPresent
                NewConstruction
        floor_to_floor: A number that represents the average distance between
            floors for the building typology.  The default is set to 3.05 meters.
        floor_area: A number that represents the floor area of the buiding in
            square meteres. The default is auto-calculated using the
            footprint_area, average_height, and floor_to_floor.
        glz_ratio: An optional number from 0 to 1 that represents the fraction
            of the walls of the building typology that are glazed. If no value
            is input here, a default will be used that comes from the DoE building
            template from the bldg_program and bldg_era.
        uwg_parameters: Optional UWG TypologyPar to set the properties of a
            building typology that specifically relate to the UWG
            (ie. roof / wall albedo, fraction of bldg heat to canyon)
    """

    def __init__(self, average_height, footprint_area, facade_area,
                 bldg_program, bldg_era, floor_to_floor=None, floor_area=None,
                 glz_ratio=None, uwg_parameters=None):
        """Initialize a dragonfly building typology"""
        # track whether the parent district geometry must be updated.
        self._has_parent_district = False
        self._parent_district = None

        # critical geometry parameters that all typologies must have.
        self.average_height = average_height
        self.footprint_area = footprint_area
        self.facade_area = facade_area
        self.floor_to_floor = floor_to_floor
        self.floor_area = floor_area

        # critical program parameters that all typologies must have.
        self.bldg_program = bldg_program
        self.bldg_era = bldg_era

        # optional parameters with default values set by building program.
        self.glz_ratio = glz_ratio
        self.uwg_parameters = uwg_parameters

    @classmethod
    def from_json(cls, data):
        """Create a typology object from a dictionary
        Args:
            data: {
                average_height: float
                footprint_area: float
                facade_area: float
                bldg_program: string
                bldg_era: string
                floor_to_floor: float
                floor_area: float
                glz_ratio: float between 0 and 1
                uwg_parameters: uwg_parameters json
            }
        """

        required_keys = ("average_height", "footprint_area", "facade_area",
                         "bldg_program", "bldg_era")

        nullable_keys = ("floor_to_floor", "floor_area", "glz_ratio",
                         "uwg_parameters")

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(
            average_height=data['average_height'],
            footprint_area=data['footprint_area'],
            facade_area=data['facade_area'],
            bldg_program=data['bldg_program'],
            bldg_era=data['bldg_era'],
            floor_to_floor=data['floor_to_floor'],
            floor_area=data['floor_area'],
            glz_ratio=data['glz_ratio'],
            uwg_parameters=TypologyPar.from_json(data['uwg_parameters'])
        )

    @classmethod
    def from_solid_geometry(cls, bldg_breps, bldg_program, bldg_era,
                            floor_to_floor=None, glz_ratio=None,
                            uwg_parameters=None):
        """Initialize a building typology from closed building brep geometry

        Args:
            bldg_breps: A list of closed rhino breps representing
                buildings of the typology.
            bldg_program: A text string representing one of the 16 DOE building
                program types to be used as a template for this typology.
            bldg_era: A text string that sets the age of the buildings represented
                by this typology.
            floor_to_floor: A number that represents the average distance between
                floors. Default is set to 3.05 meters.
            glz_ratio: An optional number from 0 to 1 that represents the fraction
                of the walls of the building typology that are glazed. Default will
                come from the DoE building template from the bldg_program and bldg_era.
            uwg_parameters: Optional UWG TypologyPar to set the properties of a
                building typology that specifically relate to the UWG
                (ie. roof / wall albedo, fraction of bldg heat to canyon)
        Returns:
            typology: The dragonfly typology object
            footprint_breps: Breps representing the footprints of the buildings.
            floor_breps: Breps representing the floors of the buildings in the typology.
            facade_breps: Breps representing the exposed facade surfaces of the typology.
        """
        assert dragonfly.isplus, \
            '"from_geometry" method can only be used in [+] libraries.'

        avg_bldg_height, footprint_area, floor_area, facade_area, footprint_breps, \
            floor_breps, facade_breps = plus.calculateTypologyGeoParams(
                bldg_breps, floor_to_floor)

        typology = cls(avg_bldg_height, footprint_area, facade_area,
                       bldg_program, bldg_era, floor_to_floor,
                       floor_area, glz_ratio, uwg_parameters)

        return typology, footprint_breps, floor_breps, facade_breps

    @classmethod
    def from_footprint_geometry(cls, bldg_footprint_breps, avg_num_stories,
                                bldg_program, bldg_era, floor_to_floor=None,
                                glz_ratio=None, uwg_parameters=None):
        """Initialize typology from building footprints and an average number of stories.

        Args:
            bldg_footprint_breps: A list of surface rhino breps representing
                the building footprints of the typology.
            avg_num_stories: A float value (greater than or equal to 1) that represents
                the average number of stories of the buildings in the typology.
            bldg_program: A text string representing one of the 16 DOE building
                program types to be used as a template for this typology.
            bldg_era: A text string that sets the age of the buildings represented
                by this typology.
            floor_to_floor: A number that represents the average distance
                between floors. Default is set to 3.05 meters.
            glz_ratio: An optional number from 0 to 1 that represents the
                fraction of the walls of the building typology that are
                glazed. Default will come from the DoE building template from
                the bldg_program and bldg_era.
            uwg_parameters: Optional UWG TypologyPar to set the properties of a
                building typology that specifically relate to the UWG
                (ie. roof / wall albedo, fraction of bldg heat to canyon)

        Returns:
            typology: The dragonfly typology object
            perimeter_curves: The exterior-exposed curves of the footprints.
        """
        assert dragonfly.isplus, \
            '"from_geometry" method can only be used in [+] libraries.'
        assert avg_num_stories >= 1, \
            'num_stories must be greater than or equal to 1. Got {}'.format(
                str(avg_num_stories))

        footprint_area, perimeter_length, perimeter_curves = \
            plus.calculateFootprintGeoParams(bldg_footprint_breps)

        if floor_to_floor is not None:
            avg_bldg_height = floor_to_floor * avg_num_stories
        else:
            avg_bldg_height = 3.05 * avg_num_stories
        facade_area = perimeter_length * avg_bldg_height
        floor_area = footprint_area * avg_num_stories

        typology = cls(avg_bldg_height, footprint_area, facade_area,
                       bldg_program, bldg_era, floor_to_floor, floor_area,
                       glz_ratio, uwg_parameters)

        return typology, perimeter_curves

    @classmethod
    def from_footprint_geo_and_stories(cls, bldg_footprint_breps, num_stories,
                                       bldg_program, bldg_era, floor_to_floor=None,
                                       glz_ratio=None, uwg_parameters=None):
        """Initialize typology from building footprints and list of building stories.

        Args:
            bldg_footprint_breps: A list of surface rhino breps representing
                the building footprints of the typology.
            num_stories: A list of integer values (all greater than or equal
                to 1) that represent the number of stories for each of the
                surfaces in the bldg_footprint_breps.
            bldg_program: A text string representing one of the 16 DOE building
                program types to be used as a template for this typology.
            bldg_era: A text string that sets the age of the buildings
                represented by this typology.
            floor_to_floor: A number that represents the average distance
                between floors. Default is set to 3.05 meters.
            glz_ratio: An optional number from 0 to 1 that represents the
                fraction of the walls of the building typology that are glazed.
                Default will come from the DoE building template from the
                bldg_program and bldg_era.
            uwg_parameters: Optional UWG TypologyPar to set the properties of a
                building typology that specifically relate to the UWG
                (ie. roof / wall albedo, fraction of bldg heat to canyon)

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
                                   bldg_program, bldg_era, floor_to_floor,
                                   glz_ratio, uwg_parameters)

    @classmethod
    def create_merged_typology(cls, typ_one, typ_two):
        """Creates a merged typology between two typologies of the same building type.

        Args:
            typ_one: The first Dragonfly building typology.
            typ_two: The second Dragonfly building typology.

        Returs:
            merged_typology: A Dragonfly typology representing the
                merged previous typologies.
        """
        # checks
        assert (hasattr(typ_one, 'isTypology')), \
            'typ_one must be a Dragonfly typology. got {}'.format(
                type(typ_one))
        assert (hasattr(typ_two, 'isTypology')), \
            'typ_two must be a Dragonfly typology. got {}'.format(
                type(typ_two))
        assert (typ_one.bldg_program == typ_two.bldg_program), \
            "bldg_program of one: {} does not match that of two: {}".format(
                typ_one.bldg_program, typ_two.bldg_program)
        assert (typ_one.bldg_era == typ_two.bldg_era), \
            "bldg_era of this one: {} does not match that of two: {}".format(
                typ_one.bldg_era, typ_two.bldg_era)

        # attributes that get totalled
        new_footprint_area = typ_one.footprint_area + typ_two.footprint_area
        new_facade_area = typ_one.facade_area + typ_two.facade_area
        new_floor_area = typ_one.floor_area + typ_two.floor_area

        # geometry atributes that get weighted averaged.
        new_average_height = (typ_one.average_height *
                              typ_one.footprint_area +
                              typ_two.average_height *
                              typ_two.footprint_area) / new_footprint_area
        new_floor_to_floor = (typ_one.floor_to_floor *
                              typ_one.floor_area +
                              typ_two.floor_to_floor *
                              typ_two.floor_area)/new_floor_area
        new_glz_ratio = (typ_one.glz_ratio * typ_one.facade_area +
                         typ_two.glz_ratio * typ_two.facade_area) / new_facade_area

        new_uwg_param = cls._create_merged_uwg_param(typ_one, typ_two,
                                                     new_floor_area,
                                                     new_facade_area,
                                                     new_footprint_area)

        # assemble the new typology object
        return cls(new_average_height, new_footprint_area, new_facade_area,
                   typ_one.bldg_program, typ_one.bldg_era, new_floor_to_floor,
                   new_floor_area, new_glz_ratio, new_uwg_param)

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
        if self.has_parent_district is True:
            self.parent_district._update_geo_from_typologies()

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
        if self.has_parent_district is True:
            self.parent_district._update_geo_from_typologies()

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
        if self.has_parent_district is True:
            self.parent_district._update_geo_from_typologies()

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
        """An integer representing the average number of stories of the buildings."""
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
        if self.has_parent_district is True:
            self.parent_district._update_geo_from_typologies()

    @property
    def bldg_program(self):
        """Get or set the program of the buildings in the typology."""
        return self._bldg_program

    @bldg_program.setter
    def bldg_program(self, prog):
        self._bldg_program = BuildingTypes.check_program(prog)

    @property
    def bldg_era(self):
        """Get or set the construction era of buildings in the typology."""
        return self._bldg_era

    @bldg_era.setter
    def bldg_era(self, age):
        self._bldg_era = BuildingTypes.check_era(age)

    @property
    def glz_ratio(self):
        """Get or set the glazing ratio of the buildings in the typology."""
        return self._glz_ratio

    @glz_ratio.setter
    def glz_ratio(self, x):
        if x is not None:
            assert isinstance(x, (float, int)), \
                'glz_ratio must be a number got {}'.format(type(x))
            self._glz_ratio = in_range(x, 0, 1, 'glz_ratio')
        else:
            self._glz_ratio = BuildingTypes.default_glazing_ratio(self.bldg_program)

    @property
    def uwg_parameters(self):
        """Get or set the uwg parameters (ie. wall/roof albedo, fract heat to canyon)."""
        return self._uwg_parameters

    @uwg_parameters.setter
    def uwg_parameters(self, uwg_par):
        if uwg_par is not None:
            assert hasattr(uwg_par, 'isTypologyPar'), \
                'uwg_parameters is not a dragonfly TypologyPar object. Got {}'.format(
                    type(uwg_par))
            self._uwg_parameters = deepcopy(uwg_par)
        else:
            self._uwg_parameters = TypologyPar()

        # Override null values with the defaults of this typology
        if self._uwg_parameters._wall_albedo is None:
            self._uwg_parameters._wall_albedo = TypologyDefaults.wall_albedo_by_type(
                self._bldg_program)
        if self._uwg_parameters._roof_albedo is None:
            self._uwg_parameters._roof_albedo = TypologyDefaults.roof_albedo_by_era(
                self.bldg_era)
        if self._uwg_parameters._shgc is None and self.has_parent_district is True:
            self._uwg_parameters._shgc = TypologyDefaults.shgc_by_era_zone(
                self.bldg_era, self._parent_district.climate_zone)

    def _create_merged_uwg_param(typ_one, typ_two, new_floor_area,
                                 new_facade_area, new_footprint_area):
        # for window properties
        _typ_one_glz_area = typ_one.facade_area * typ_one.glz_ratio
        _typ_two_glz_area = typ_two.facade_area * typ_two.glz_ratio

        # uwg_parameters that get weighted averaged
        new_fract_heat_to_canyon = (typ_one.uwg_parameters.fract_heat_to_canyon *
                                    typ_one.floor_area +
                                    typ_two.uwg_parameters.fract_heat_to_canyon *
                                    typ_two.floor_area) / new_floor_area
        new_wall_albedo = (typ_one.uwg_parameters.wall_albedo *
                           typ_one.facade_area +
                           typ_two.uwg_parameters.wall_albedo *
                           typ_two.facade_area) / new_facade_area
        new_roof_albedo = (typ_one.uwg_parameters.roof_albedo *
                           typ_one.footprint_area +
                           typ_two.uwg_parameters.roof_albedo *
                           typ_two.footprint_area) / new_footprint_area
        new_roof_veg_fraction = (typ_one.uwg_parameters.roof_veg_fraction *
                                 typ_one.footprint_area +
                                 typ_two.uwg_parameters.roof_veg_fraction *
                                 typ_two.footprint_area) / new_footprint_area
        if typ_one.uwg_parameters.shgc is not None \
                and typ_one.uwg_parameters.shgc is not None:
                    new_shgc = (typ_one.uwg_parameters.shgc * _typ_one_glz_area +
                                typ_two.uwg_parameters.shgc * _typ_two_glz_area
                                ) / (_typ_one_glz_area + _typ_two_glz_area)
        else:
            new_shgc = None
        return TypologyPar(new_fract_heat_to_canyon, new_shgc, new_wall_albedo,
                           new_roof_albedo, new_roof_veg_fraction)

    @property
    def has_parent_district(self):
        return self._has_parent_district

    @property
    def parent_district(self):
        return self._parent_district

    @property
    def isTypology(self):
        """Return True for Typology."""
        return True

    def to_json(self):
        """Create a typology dictionary
        Results:
            {
                average_height: float
                footprint_area: float
                facade_area: float
                bldg_program: string
                bldg_era: string
                floor_to_floor: float
                floor_area: float
                glz_ratio: float between 0 and 1
                uwg_parameters: uwg_parameters json
            }
        """
        return {
            "average_height": self.average_height,
            "footprint_area": self.footprint_area,
            "facade_area": self.facade_area,
            "bldg_program": self.bldg_program,
            "bldg_era": self.bldg_era,
            "floor_to_floor": self.floor_to_floor,
            "floor_area": self.floor_area,
            "glz_ratio": self.glz_ratio,
            "uwg_parameters": self.uwg_parameters.to_json()
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly typology."""
        return 'Building Typology: ' \
               '\n  {}, {}' \
               '\n  Average Height: {} m' \
               '\n  Number of Stories: {}' \
               '\n  Floor Area: {:,.0f} m2' \
               '\n  Footprint Area: {:,.0f} m2' \
               '\n  Facade Area: {:,.0f} m2' \
               '\n  Glazing Ratio: {} %'.format(
                   self._bldg_program, self._bldg_era,
                   int(self._average_height), self.number_of_stories,
                   self.floor_area, self.footprint_area,
                   self.facade_area, int(self.glz_ratio*100)
               )
