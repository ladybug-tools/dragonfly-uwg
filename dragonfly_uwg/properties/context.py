# coding=utf-8
"""Context Shade UWG Properties."""


class ContextShadeUWGProperties(object):
    """UWG Properties for Dragonfly ContextShade.

    Args:
        host_shade: A dragonfly_core ContextShade object that hosts these properties.
        is_vegetation: Boolean to note whether the shade represents a tree canopy,
            in which case, it will be incorporated into the simulation as tree
            cover. (Default: False).

    Properties:
        * host
        * is_vegetation
    """

    __slots__ = ('_host', '_is_vegetation')

    def __init__(self, host_shade, is_vegetation=False):
        """Initialize ContextShade UWG properties."""
        self._host = host_shade
        self.is_vegetation = is_vegetation

    @property
    def host(self):
        """Get the Shade object hosting these properties."""
        return self._host

    @property
    def is_vegetation(self):
        """Get or set a boolean for whether the shade represents a tree canopy."""
        return self._is_vegetation

    @is_vegetation.setter
    def is_vegetation(self, value):
        self._is_vegetation = bool(value)

    @classmethod
    def from_dict(cls, data, host):
        """Create ContextShadeUWGProperties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of ContextShadeUWGProperties.
            host: A ContextShade object that hosts these properties.
        """
        assert data['type'] == 'ContextShadeUWGProperties', \
            'Expected ContextShadeUWGProperties. Got {}.'.format(data['type'])
        is_veg = data['is_vegetation'] if 'is_vegetation' in data else False
        return cls(host, is_veg)

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a ContextShadeUWGPropertiesAbridged dictionary.

        Args:
            abridged_data: A ContextShadeUWGPropertiesAbridged dictionary (typically
                coming from a Model).
        """
        if 'is_vegetation' in abridged_data:
            self.is_vegetation = abridged_data['is_vegetation']

    def to_dict(self, abridged=False):
        """Return UWG properties as a dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
        """
        base = {'uwg': {}}
        base['uwg']['type'] = 'ContextShadeUWGProperties' if not \
            abridged else 'ContextShadeUWGPropertiesAbridged'
        base['uwg']['is_vegetation'] = self.is_vegetation
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new ContextShade object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return ContextShadeUWGProperties(_host, self._is_vegetation)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Context Shade UWG Properties: {}'.format(self.host.identifier)
