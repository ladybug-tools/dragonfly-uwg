# coding=utf-8
"""Story UWG Properties."""


class StoryUWGProperties(object):
    """UWG Properties for Dragonfly Story.

    Args:
        host: A dragonfly_core Story object that hosts these properties.

    Properties:
        * host
    """

    __slots__ = ('_host',)

    def __init__(self, host):
        """Initialize Story UWG properties."""
        self._host = host

    @property
    def host(self):
        """Get the Story object hosting these properties."""
        return self._host

    @classmethod
    def from_dict(cls, data, host):
        """Create StoryUWGProperties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of StoryUWGProperties.
            host: A Story object that hosts these properties.
        """
        assert data['type'] == 'StoryUWGProperties', \
            'Expected StoryUWGProperties. Got {}.'.format(data['type'])
        new_prop = cls(host)
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a StoryUWGPropertiesAbridged dictionary.

        Args:
            abridged_data: A StoryUWGPropertiesAbridged dictionary (typically
                coming from a Model).
        """
        pass  # currently no properties to apply

    def to_dict(self, abridged=False):
        """Return Story UWG properties as a dictionary.

        Args:
            abridged: Boolean for whether the full dictionary of the Story should
                be written (False) or just the identifier of the the individual
                properties (True). Default: False.
        """
        base = {'uwg': {}}
        base['uwg']['type'] = 'StoryUWGProperties' if not \
            abridged else 'StoryUWGPropertiesAbridged'
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new Story object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return StoryUWGProperties(_host)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Story UWG Properties: {}'.format(self.host.identifier)
