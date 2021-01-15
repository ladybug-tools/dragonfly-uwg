# coding=utf-8
from __future__ import division

from honeybee.typing import float_in_range, int_in_range
from honeybee.altnumber import autocalculate


class VegetationParameter(object):
    """Represents the behavior of vegetation within an urban area.

    Args:
        vegetation_albedo: A number between 0 and 1 that represents
            the ratio of reflected radiation from vegetated surfaces
            to incident radiation upon them. (Default: 0.25)
        start_month: An integer from 1 to 12 that represents the month
            at which vegetation evapostranspiration begins (leaves come out).
            If Autocalculate, the month will be automatically determined by analyzing
            the epw to see which months have an average monthly temperature
            above 10C. (Default: autocalculate).
        end_month: An integer from 1 to 12 that represents the month
            at which vegetation evapostranspiration ends (leaves fall off).
            If Autocalculate, the month will be automatically determined by analyzing
            the epw to see which months have an average monthly temperature
            above 10C. (Default: autocalculate).
        tree_latent_fraction: A number between 0 and 1 that represents
            the the fraction of absorbed solar energy by trees that
            is given off as latent heat (evapotranspiration). Currently,
            this does not affect the moisture balance in the uwg but
            it will affect the temperature. (Default: 0.7).
        grass_latent_fraction: A number between 0 and 1 that represents
            the the fraction of absorbed solar energy by grass that is
            given off as latent heat (evapotranspiration). Currently,
            this does not affect the moisture balance in the uwg but
            it will affect the temperature. (Default: 0.5).
    """

    __slots__ = ('_vegetation_albedo', '_start_month', '_end_month',
                 '_tree_latent_fraction', '_grass_latent_fraction')

    def __init__(self, vegetation_albedo=0.25, start_month=autocalculate,
                 end_month=autocalculate,
                 tree_latent_fraction=0.7, grass_latent_fraction=0.5):
        """Initialize dragonfly vegetation parameters"""
        self.vegetation_albedo = vegetation_albedo
        self.start_month = start_month
        self.end_month = end_month
        self.tree_latent_fraction = tree_latent_fraction
        self.grass_latent_fraction = grass_latent_fraction

    @classmethod
    def from_dict(cls, data):
        """Create a VegetationParameter object from a dictionary

        Args:
            data: A dictionary representation of an VegetationParameter object
                in the format below.

        .. code-block:: python

            {
            'type': 'VegetationParameter',
            'vegetation_albedo': 0.3,  # float between 0 and 1
            'start_month': 5,  # int between 1 and 12
            'end_month': 10,  # int between 1 and 12
            'tree_latent_fraction': 0.75, # float between 0 and 1
            'grass_latent_fraction': 0.45  # float between 0 and 1
            }
        """
        alb = data['vegetation_albedo'] if 'vegetation_albedo' in data else 0.25
        start = autocalculate if 'start_month' not in data or \
            data['start_month'] == autocalculate.to_dict() else data['start_month']
        end = autocalculate if 'end_month' not in data or \
            data['end_month'] == autocalculate.to_dict() else data['end_month']
        tree = data['tree_latent_fraction'] if 'tree_latent_fraction' in data else 0.7
        grass = data['grass_latent_fraction'] if 'grass_latent_fraction' in data else 0.5
        return cls(alb, start, end, tree, grass)

    @property
    def vegetation_albedo(self):
        """Get or set a fractional number for the vegetation albedo."""
        return self._vegetation_albedo

    @vegetation_albedo.setter
    def vegetation_albedo(self, value):
        self._vegetation_albedo = float_in_range(value, 0, 1, 'vegetation_albedo')

    @property
    def start_month(self):
        """Get or set an integer (or Autocalculate) for the vegetation start month."""
        return self._start_month if self._start_month is not None else autocalculate

    @start_month.setter
    def start_month(self, value):
        if value == autocalculate:
            self._start_month = None
        else:
            self._start_month = \
                int_in_range(value, 1, 12, 'start_month')

    @property
    def end_month(self):
        """Get or set an integer (or Autocalculate) for the vegetation end month."""
        return self._end_month if self._end_month is not None \
            else autocalculate

    @end_month.setter
    def end_month(self, value):
        if value == autocalculate:
            self._end_month = None
        else:
            self._end_month = \
                int_in_range(value, 1, 12, 'end_month')

    @property
    def tree_latent_fraction(self):
        """Get or set a number for the tree latent fraction."""
        return self._tree_latent_fraction

    @tree_latent_fraction.setter
    def tree_latent_fraction(self, value):
        self._tree_latent_fraction = float_in_range(value, 0, 1, 'tree_latent_fraction')

    @property
    def grass_latent_fraction(self):
        """Get or set a number for the grass latent fraction."""
        return self._grass_latent_fraction

    @grass_latent_fraction.setter
    def grass_latent_fraction(self, value):
        self._grass_latent_fraction = \
            float_in_range(value, 0, 1, 'grass_latent_fraction')

    def to_dict(self):
        """Get VegetationParameter dictionary."""
        base = {'type': 'VegetationParameter'}
        base['vegetation_albedo'] = self.vegetation_albedo
        base['tree_latent_fraction'] = self.tree_latent_fraction
        base['grass_latent_fraction'] = self.grass_latent_fraction
        if self._start_month is not None:
            base['start_month'] = self._start_month
        if self._end_month is not None:
            base['end_month'] = self._end_month
        return base

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        new_obj = VegetationParameter(self._vegetation_albedo)
        new_obj._tree_latent_fraction = self._tree_latent_fraction
        new_obj._grass_latent_fraction = self._grass_latent_fraction
        new_obj._start_month = self._start_month
        new_obj._end_month = self._end_month
        return new_obj

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Represent Dragonfly vegetation parameters."""
        return 'VegetationParameter: [albedo: {}]  [tree latent: {}] [grass latent:' \
            ' {}]'.format(self._vegetation_albedo, self._tree_latent_fraction,
                          self._grass_latent_fraction)
