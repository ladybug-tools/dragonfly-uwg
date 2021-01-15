
from dragonfly_uwg.properties.building import BuildingUWGProperties

from dragonfly.building import Building
from honeybee.altnumber import autocalculate

from tests.fixtures.building import default_building, custom_building


def test_uwg_properties():
    """Test the existence of the Building UWG properties."""
    building = default_building()

    assert hasattr(building.properties, 'uwg')
    assert isinstance(building.properties.uwg, BuildingUWGProperties)
    str(building.properties.uwg)  # test the string representation
    assert isinstance(building.properties.host, Building)
    assert building.properties.uwg.program == 'LargeOffice'
    assert building.properties.uwg.vintage == 'New'
    assert building.properties.uwg.fract_heat_to_canyon == 0.5
    assert building.properties.uwg.shgc == autocalculate
    assert building.properties.uwg.wall_albedo == 0.08
    assert building.properties.uwg.roof_albedo == 0.7
    assert building.properties.uwg.roof_veg_fraction == 0


def test_duplicate():
    """Test the duplicate method."""
    building = custom_building()
    new_building = building.duplicate()
    assert new_building is not building

    assert new_building.properties.uwg.program == building.properties.uwg.program
    assert new_building.properties.uwg.vintage == building.properties.uwg.vintage
    assert new_building.properties.uwg.fract_heat_to_canyon == \
        building.properties.uwg.fract_heat_to_canyon
    assert new_building.properties.uwg.shgc == building.properties.uwg.shgc
    assert new_building.properties.uwg.wall_albedo == building.properties.uwg.wall_albedo
    assert new_building.properties.uwg.roof_albedo == building.properties.uwg.roof_albedo
    assert new_building.properties.uwg.roof_veg_fraction == \
        building.properties.uwg.roof_veg_fraction


def test_to_from_dict():
    """Test the Building to_dict and from_dict methods."""
    building = custom_building()

    building_dict = building.to_dict()

    assert 'uwg' in building_dict['properties']
    assert 'program' in building_dict['properties']['uwg']
    assert 'vintage' in building_dict['properties']['uwg']
    assert 'fract_heat_to_canyon' in building_dict['properties']['uwg']

    new_building = Building.from_dict(building_dict)

    assert new_building.properties.uwg.program == building.properties.uwg.program
    assert new_building.properties.uwg.vintage == building.properties.uwg.vintage
    assert new_building.properties.uwg.fract_heat_to_canyon == \
        building.properties.uwg.fract_heat_to_canyon
    assert new_building.properties.uwg.shgc == building.properties.uwg.shgc
    assert new_building.properties.uwg.wall_albedo == building.properties.uwg.wall_albedo
    assert new_building.properties.uwg.roof_albedo == building.properties.uwg.roof_albedo
    assert new_building.properties.uwg.roof_veg_fraction == \
        building.properties.uwg.roof_veg_fraction
