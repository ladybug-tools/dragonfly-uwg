# coding=utf-8
from honeybee.typing import float_in_range, float_positive
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug_geometry.geometry2d.polygon import Polygon2D
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D

import math


class Terrain(object):
    """Object representing the terrain on which an urban area sits.

    Note:
        [1] Street, Michael A. (2013). Comparison of simplified models of urban
        climate for improved prediction of building energy use in cities. Thesis
        (S.M. in Building Technology) - Massachusetts Institute of Technology,
        Dept. of Architecture, http://hdl.handle.net/1721.1/82284

    Args:
        geometry: An array of ladybug_geometry Face3D objects that together
            represent the terrian. This should include the entire area of the
            site, including that beneath building footprints.
        pavement_albedo: A number between 0 and 1 that represents the albedo
            (reflectivity) of the pavement. (Default: 0.1, typical of fresh asphalt).
        pavement_thickness: A number that represents the thickness of the
            pavement material in meters. (Default: 0.5 meters).
        pavement_conductivity: A number representing the conductivity of the pavement
            material in W/m-K. (Default: 1 W/m-K, typical of asphalt).
        pavement_heat_capacity: A number representing the volumetric heat
            capacity of the pavement material in J/m3-K. This is the number
            of joules needed to raise one cubic meter of the material by 1 degree
            Kelvin. (Default: 1.6e6 J/m3-K, typical of asphalt).

    Properties:
        * geometry
        * pavement_albedo
        * pavement_thickness
        * pavement_conductivity
        * pavement_heat_capacity
        * polygon2ds
        * area
        * horizontal_area
        * characteristic_length
        * min
        * max
    """
    __slots__ = ('_geometry', '_polygon2ds', '_pavement_albedo', '_pavement_thickness',
                 '_pavement_conductivity', '_pavement_heat_capacity')

    def __init__(self, geometry, pavement_albedo=0.1, pavement_thickness=0.5,
                 pavement_conductivity=1.0, pavement_heat_capacity=1.6e6):
        """Initialize a dragonfly Terrain"""
        # process the geometry
        if not isinstance(geometry, tuple):
            geometry = tuple(geometry)
        assert len(geometry) > 0, 'Terrain must have at least one Face3D.'
        for geo in geometry:
            assert isinstance(geo, Face3D), \
                'Expected ladybug_geometry Face3D. Got {}'.format(type(geo))
        self._geometry = geometry
        self._polygon2ds = None

        # process the other parameters
        self.pavement_albedo = pavement_albedo
        self.pavement_thickness = pavement_thickness
        self.pavement_conductivity = pavement_conductivity
        self.pavement_heat_capacity = pavement_heat_capacity

    @classmethod
    def from_building_bounding_rect(cls, buildings):
        """Initialize a Terrain from a list of dragonfly Buildings.

        Args:
            buildings: An array of dragonfly Buildings around which a bounding
                rectangle will be computed to produce terrain geometry.
        """
        # figure out the min and max Point2D around all of the geometry
        min_pt, max_pt = buildings[0].min, buildings[0].max
        min_pt, max_pt = [min_pt.x, min_pt.y], [max_pt.x, max_pt.y]
        for bldg in buildings[1:]:
            bldg_min, bldg_max = bldg.min, bldg.max
            if bldg_min.x < min_pt[0]:
                min_pt[0] = bldg_min.x
            if bldg_min.y < min_pt[1]:
                min_pt[1] = bldg_min.y
            if bldg_max.x > max_pt[0]:
                max_pt[0] = bldg_max.x
            if bldg_max.y > max_pt[1]:
                max_pt[1] = bldg_max.y
        # convert the min and max into a Face3D
        base, height = max_pt[0] - min_pt[0], max_pt[1] - min_pt[1]
        base_plane = Plane(o=Point3D(min_pt[0], min_pt[1], 0))
        return cls((Face3D.from_rectangle(base, height, base_plane),))

    @classmethod
    def from_dict(cls, data):
        """Initialize a Terrain from a dictionary.

        Args:
            data: A dictionary representation of a Terrain object in the format below.

        .. code-block:: python

            {
            "type": 'Terrain',
            "geometry": [],  # array for Face3D for the terrain surface
            "pavement_albedo": 0.15,  # number for the pavement albedo
            "pavement_thickness": 0.75,  # pavement thickness in meters
            "pavement_conductivity": 1.0,  # pavement conductivity in W/m2-K
            "pavement_heat_capacity": 1600000  # volumetric heat capacity in J/m3-K
            }
        """
        # check the type of dictionary
        assert data['type'] == 'Terrain', 'Expected Terrain dictionary. ' \
            'Got {}.'.format(data['type'])
        # process the geometry
        geometry = tuple(Face3D.from_dict(geo) for geo in data['geometry'])
        # process the other parameters
        alb = data['pavement_albedo'] if 'pavement_albedo' in data else 0.1
        thick = data['pavement_thickness'] if 'pavement_thickness' in data else 0.5
        cond = data['pavement_conductivity'] if 'pavement_conductivity' in data else 1.0
        h_cap = data['pavement_heat_capacity'] \
            if 'pavement_heat_capacity' in data else 1.6e6
        return cls(geometry, alb, thick, cond, h_cap)

    @property
    def geometry(self):
        """Get a tuple of Face3D objects that together represent the Terrain."""
        return self._geometry

    @property
    def pavement_albedo(self):
        """Get or set a number between 0 and 1 for the pavement albedo (reflectivity)."""
        return self._pavement_albedo

    @pavement_albedo.setter
    def pavement_albedo(self, value):
        self._pavement_albedo = float_in_range(value, 0, 1, 'pavement_albedo')

    @property
    def pavement_thickness(self):
        """Get or set a number for the pavement thickness in meters."""
        return self._pavement_thickness

    @pavement_thickness.setter
    def pavement_thickness(self, value):
        self._pavement_thickness = float_positive(value, 'pavement_thickness')

    @property
    def pavement_conductivity(self):
        """Get or set a number for the pavement conductivity in W/m-K."""
        return self._pavement_conductivity

    @pavement_conductivity.setter
    def pavement_conductivity(self, value):
        self._pavement_conductivity = float_positive(value, 'pavement_conductivity')

    @property
    def pavement_heat_capacity(self):
        """Get or set a number for the pavement volumetric heat capacity in J/m3-K."""
        return self._pavement_heat_capacity

    @pavement_heat_capacity.setter
    def pavement_heat_capacity(self, value):
        self._pavement_heat_capacity = float_positive(value, 'pavement_heat_capacity')

    @property
    def polygon2ds(self):
        """Get a tuple of Polygon2D objects that together represent the Terrain."""
        if self._polygon2ds is None:
            self._polygon2ds = self._face3d_to_polygon2d(self._geometry)
        return self._polygon2ds

    @property
    def area(self):
        """Get a number for the total surface area of the Terrain."""
        return sum([geo.area for geo in self._geometry])

    @property
    def horizontal_area(self):
        """Get a number for the horizontal area of the urban Terrain surface.

        This is projected into the XY plane.
        """
        return sum([geo.area for geo in self.polygon2ds])

    @property
    def characteristic_length(self):
        """Get a number for the characteristic length.

        This is the linear dimension of the side of a square that encompasses
        the neighborhood.
        """
        return math.sqrt(self.horizontal_area)

    @property
    def min(self):
        """Get a Point2D for the min bounding rectangle vertex in the XY plane."""
        return self._calculate_min(self._geometry)

    @property
    def max(self):
        """Get a Point2D for the max bounding rectangle vertex in the XY plane."""
        return self._calculate_max(self._geometry)

    def move(self, moving_vec):
        """Move this Terrain along a vector.

        Args:
            moving_vec: A ladybug_geometry Vector3D with the direction and distance
                to move the object.
        """
        self._geometry = tuple(geo.move(moving_vec) for geo in self._geometry)
        self._polygon2ds = None

    def rotate_xy(self, angle, origin):
        """Rotate this Terrain counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        self._geometry = tuple(geo.rotate_xy(math.radians(angle), origin)
                               for geo in self._geometry)
        self._polygon2ds = None

    def reflect(self, plane):
        """Reflect this Terrain across a plane.

        Args:
            plane: A ladybug_geometry Plane across which the object will be reflected.
        """
        self._geometry = tuple(geo.reflect(plane.n, plane.o)
                               for geo in self._geometry)
        self._polygon2ds = None

    def scale(self, factor, origin=None):
        """Scale this Terrain by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point3D representing the origin from which
                to scale. If None, it will be scaled from the World origin (0, 0, 0).
        """
        self._geometry = tuple(geo.scale(factor, origin)
                               for geo in self._geometry)
        self._polygon2ds = None

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def to_dict(self):
        """Get Terrain as a dictionary."""
        base = {'type': 'Terrain'}
        base['geometry'] = [geo.to_dict(False) for geo in self._geometry]
        base['pavement_albedo'] = self.pavement_albedo
        base['pavement_thickness'] = self.pavement_thickness
        base['pavement_conductivity'] = self.pavement_conductivity
        base['pavement_heat_capacity'] = self.pavement_heat_capacity
        return base

    @staticmethod
    def _face3d_to_polygon2d(geometry):
        """Convert a list of Face3D into Polygon2D in the XY Plane."""
        vert2ds = ((Point2D(pt.x, pt.y) for pt in poly) for poly in geometry)
        return tuple(Polygon2D(poly) for poly in vert2ds)

    @staticmethod
    def _calculate_min(geometry_objects):
        """Calculate min Point2D around an array of geometry with min attributes.

        This is used in all functions that calculate bounding rectangles around
        dragonfly objects and assess when two objects are in close proximity.
        """
        min_pt = [geometry_objects[0].min.x, geometry_objects[0].min.y]

        for room in geometry_objects[1:]:
            if room.min.x < min_pt[0]:
                min_pt[0] = room.min.x
            if room.min.y < min_pt[1]:
                min_pt[1] = room.min.y

        return Point2D(min_pt[0], min_pt[1])

    @staticmethod
    def _calculate_max(geometry_objects):
        """Calculate max Point2D around an array of geometry with max attributes.

        This is used in all functions that calculate bounding rectangles around
        dragonfly objects and assess when two objects are in close proximity.
        """
        max_pt = [geometry_objects[0].max.x, geometry_objects[0].max.y]

        for room in geometry_objects[1:]:
            if room.max.x > max_pt[0]:
                max_pt[0] = room.max.x
            if room.max.y > max_pt[1]:
                max_pt[1] = room.max.y

        return Point2D(max_pt[0], max_pt[1])

    def __copy__(self):
        new_obj = Terrain(self._geometry)
        new_obj._polygon2ds = self._polygon2ds
        new_obj._pavement_albedo = self._pavement_albedo
        new_obj._pavement_thickness = self._pavement_thickness
        new_obj._pavement_conductivity = self._pavement_conductivity
        new_obj._pavement_heat_capacity = self._pavement_heat_capacity
        return new_obj

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represent Dragonfly Terrain."""
        return 'Terrain: [{} faces]'.format(len(self._geometry))
