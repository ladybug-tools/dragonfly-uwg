from dragonfly_uwg.properties.context import ContextShadeUWGProperties

from dragonfly.context import ContextShade

from tests.fixtures.context import default_context, custom_context


def test_uwg_properties():
    """Test the existence of the ContextShade UWG properties."""
    context = default_context()

    assert hasattr(context.properties, 'uwg')
    assert isinstance(context.properties.uwg, ContextShadeUWGProperties)
    str(context.properties.uwg)  # test the string representation
    assert isinstance(context.properties.host, ContextShade)
    assert not context.properties.uwg.is_vegetation


def test_duplicate():
    """Test the duplicate method."""
    context = custom_context()
    new_context = context.duplicate()
    assert new_context is not context

    assert new_context.properties.uwg.is_vegetation == \
        context.properties.uwg.is_vegetation


def test_to_from_dict():
    """Test the Building to_dict and from_dict methods."""
    context = custom_context()

    context_dict = context.to_dict()

    assert 'uwg' in context_dict['properties']
    assert 'is_vegetation' in context_dict['properties']['uwg']

    new_context = ContextShade.from_dict(context_dict)
    assert new_context.properties.uwg.is_vegetation == \
        context.properties.uwg.is_vegetation
