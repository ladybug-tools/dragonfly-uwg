# coding=utf-8
from .dfobject import DFObject
import dragonfly
try:
    import plus
except ImportError as e:
    if dragonfly.isplus:
        raise ImportError(e)

import math


class Terrain(DFObject):
    """Represents the terrain on which an urban area sits.

    Properties:
        area: The area of the urban terrain surface in square meters
            (projected into the XY plane).
        characteristic_length:  A number representing the linear dimension
            of the side of a square that encompasses the neighborhood in meters.

            The default is set to 500 m, which was found to be the recomendation
            for a typical mid-density urban area.
            Street, Michael A. (2013). Comparison of simplified models of urban
            climate for improved prediction of building energy use in cities.
            Thesis (S.M. in Building Technology)--Massachusetts Institute of
            Technology, Dept. of Architecture,
            http://hdl.handle.net/1721.1/82284
    """

    def __init__(self, area, characteristic_length=None):
        """Initialize a dragonfly terrain surface"""
        self.area = area
        self.characteristic_length = characteristic_length

    @classmethod
    def from_json(cls, data):
        """Create a terrain object from a dictionary
        Args:
            data: {
                area: float
                characteristic_length: float
            }
        """

        required_keys = ("area",)
        nullable_keys = ("characteristic_length",)

        for key in required_keys:
            assert key in data.keys(), "{} is a required value".format(key)

        for key in nullable_keys:
            if key not in data:
                data[key] = None

        return cls(area=data["area"],
                   characteristic_length=data["characteristic_length"])

    @classmethod
    def from_geometry(cls, terrainSrfs):
        """Initialize a dragonfly terrain surface from a list of terrain breps
        Args:
            terrainSrfs: A list of Rhino surfaces representing the terrian.

        Returns:
            terrain: The dragonfly terrain object.
            surfaceBreps: The srfBreps representing the terrain
                (projected into the XY plane).
        """
        surfaceArea, surfaceBreps = plus.calculateFootprints(terrainSrfs)
        terrain = cls(surfaceArea)

        return terrain, surfaceBreps

    @property
    def area(self):
        """Get or set the area of the terrain surface in the XY plane."""
        return self._area

    @area.setter
    def area(self, a):
        assert isinstance(a, (float, int)), \
            'area must be a number got {}'.format(type(a))
        assert (a >= 0), "area must be greater than 0"
        self._area = a

    @property
    def characteristic_length(self):
        """Return the characteristic length."""
        return self._characteristic_length

    @characteristic_length.setter
    def characteristic_length(self, cl):
        if cl is None:
            self._characteristic_length = math.sqrt(self._area)
        else:
            assert isinstance(cl, (float, int)),\
                'characteristic length must be a number got {}'.format(type(cl))
            assert (cl >= 0), 'characteristic length must be greater than 0'
            self._characteristic_length = cl

    @property
    def isTerrain(self):
        """Return True for Terrain."""
        return True

    def to_json(self):
        """Create a terrain dictionary
        Results:
            {
                area: float
                characteristic_length: float
            }
        """

        return {
            "area": self.area,
            "characteristic_length": self.characteristic_length
        }

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly terrain."""
        return 'Terrain:\n  Area: {} m2'.format(int(self._area))
