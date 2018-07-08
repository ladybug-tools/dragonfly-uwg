# coding=utf-8


class DfObject(object):
    """Base class for Dragonfly typology, city, terrain, and vegetation."""

    @property
    def isDfObject(self):
        """Return True."""
        return True
