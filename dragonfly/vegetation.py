# coding=utf-8
from __future__ import division

from .dfobject import DfObject
from .utilities import Utilities
import dragonfly
try:
    import plus
except ImportError as e:
    if dragonfly.isplus:
        raise ImportError(e)

class Vegetation(DfObject):
    """Represents vegetation (either grass or trees) within an urban area.

    Properties:
        area: The area of the urban terrain covered by the vegetation in square meters
            (projected into the XY plane).
        is_trees: A boolean value that denotes whether the vegetation object represents
            trees (True) or grass (False).
    """

    def __init__(self, area, is_trees=False):
        """Initialize a dragonfly vegetation object"""
        self.area = area
        self._s_trees = is_trees

    @classmethod
    def from_geometry(cls, veg_breps, is_trees=False):
        """Initialize a dragonfly tree object from a list of closed tree breps

        Args:
            veg_breps: A list of closed Rhino breps representing the tree canopy.
            is_trees: A boolean value that denotes whether the vegetation object
                represents trees (True) or grass (False).

        Returns:
            vegetation: The dragonfly vegetation object.
            projected_breps: The veg_breps projected into the XY plane.
        """
        surfaceArea, projected_breps = plus.calculateFootprints(veg_breps)
        vegetation = cls(surfaceArea, is_trees)

        return vegetation, projected_breps

    @property
    def area(self):
        """Get or set the area of the vegetation in the XY plane."""
        return self._area

    @area.setter
    def area(self, a):
        assert isinstance(a, (float, int)), \
            'area must be a number got {}'.format(type(a))
        assert (a >= 0), "area must be greater than 0"
        self._area = a

    @property
    def is_trees(self):
        """Get or set whether vegetation represents trees (True) or grass (False)."""
        return self._is_trees

    @is_trees.setter
    def is_trees(self, a):
        assert isinstance(a, (bool)), \
            'is_trees must be a boolean got {}'.format(type(a))
        self._is_trees = a

    @property
    def isVegetation(self):
        """Return True for Vegetation."""
        return True

    def computeCoverage(self, terrain):
        """Compute the coverage of the vegetation over a terrain surface.

        Args:
            terrain: A dragonfly terrin object with which to compute coverage.

        Returns:
            coverage: A number between 0 and 1 representing the fraction of
                the terrain covered by the vegetation.
        """
        assert hasattr(terrain, 'isTerrain'), \
            'terrain must be Df terrain. Got {}'.format(type(terrain))
        coverage = Utilities.in_range((self._area/terrain.area), 0, 1, 'vegetation_coverage')

        return coverage

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represnt Dragonfly vegetation."""
        vegType = 'Trees' if self._is_trees else 'Grass'
        return 'Vegetation: ' + vegType + \
               '\n  Area: ' + str(int(self._area)) + " m2"
