# coding=utf-8


class DFObject(object):
    """Base class for Dragonfly typology, district, terrain, and vegetation."""

    @property
    def isDFObject(self):
        """Return True."""
        return True


class DFParameter(object):
    """Base class for Dragonfly BuildingPar, TrafficPar, VegetationPar, etc."""

    @property
    def isDFParameter(self):
        """Return True."""
        return True
