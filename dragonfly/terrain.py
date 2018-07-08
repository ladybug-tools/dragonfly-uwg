# coding=utf-8
from dfobject import DfObject
import dragonfly
try:
    import plus
except ImportError as e:
    if dragonfly.isplus:
        raise ImportError(e)

import math


class Terrain(DfObject):
    """Represents the terrain on which an urban area sits.

    Properties:
        area: The area of the urban terrain surface in square meters
            (projected into the XY plane).
        characteristic_length:  A number representing the radius of a
            circle that encompasses the whole neighborhood in meters.
            If no value is input here, it will be auto-calculated
            assuming that the area above is square.
    """

    def __init__(self, area, characteristic_length=None):
        """Initialize a dragonfly terrain surface"""
        self.area = area

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
        self._characteristic_length = math.sqrt(self._area)

    @property
    def characteristic_length(self):
        """Return the characteristic length."""
        return self._characteristic_length

    @property
    def isTerrain(self):
        """Return True for Terrain."""
        return True

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly terrain."""
        return 'Terrain: ' + \
               '\n  Area: ' + str(int(self._area)) + " m2" + \
               '\n  Radius: ' + str(int(self._characteristic_length)) + " m"
