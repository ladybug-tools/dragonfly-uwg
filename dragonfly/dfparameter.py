# coding=utf-8


class DfParameter(object):
    """Base class for Dragonfly trafficPar, vegetationPar, pavementPar, etc."""

    @property
    def isDfParameter(self):
        """Return True."""
        return True
