from __future__ import division

from dragonfly.city import City
from dragonfly.typology import Typology
from dragonfly.terrain import Terrain
import pytest
from tests.fixtures.city import correct, default, from_typology


def test_initialise(correct):
    city = City(
        average_bldg_height=correct['average_bldg_height'],
        site_coverage_ratio=correct['site_coverage_ratio'],
        facade_to_site_ratio=correct['facade_to_site_ratio'],
        bldg_type_ratios=correct['bldg_type_ratios'],
        climate_zone=correct['climate_zone'],
        tree_coverage_ratio=correct['tree_coverage_ratio'],
        grass_coverage_ratio=correct['grass_coverage_ratio'],
        characteristic_length=correct['characteristic_length'],
        vegetation_parameters=correct['vegetation_parameters'],
        pavement_parameters=correct['pavement_parameters'],
        traffic_parameters=correct['traffic_parameters']
    )

    assert city.average_bldg_height == correct['average_bldg_height']
    assert city.site_coverage_ratio == correct['site_coverage_ratio']
    assert city.facade_to_site_ratio == correct['facade_to_site_ratio']
    assert city.bldg_type_ratios == correct['bldg_type_ratios']
    assert city.climate_zone == correct['climate_zone']
    assert city.tree_coverage_ratio == correct['tree_coverage_ratio']
    assert city.grass_coverage_ratio == correct['grass_coverage_ratio']
    assert city.characteristic_length == correct['characteristic_length']
    assert city.vegetation_parameters == correct['vegetation_parameters']
    assert city.pavement_parameters == correct['pavement_parameters']
    assert city.traffic_parameters == correct['traffic_parameters']


def test_from_typologies(from_typology):
    city = City.from_typologies(typologies=from_typology['typologies'],
                                terrain=from_typology['terrain'],
                                climate_zone=from_typology['climate_zone'],
                                tree_coverage_ratio=from_typology['tree_coverage_ratio'],
                                grass_coverage_ratio=from_typology['grass_coverage_ratio'],
                                vegetation_parameters=from_typology['vegetation_parameters'],
                                pavement_parameters=from_typology['pavement_parameters'],
                                traffic_parameters=from_typology['traffic_parameters'])

    assert city.average_bldg_height == 35
    assert city.site_coverage_ratio == 45*2 / 300
    assert city.facade_to_site_ratio == 33*2 / 300
    assert city.bldg_type_ratios =={'Hospital,1980sPresent': 0.5,
                                    'SmallOffice,NewConstruction': 0.5}
    assert city.climate_zone == from_typology['climate_zone']
    assert city.tree_coverage_ratio == from_typology['tree_coverage_ratio']
    assert city.grass_coverage_ratio == from_typology['grass_coverage_ratio']
    # assert city.characteristic_length == 17.32 # TODO: Add proper check for this value
    assert city.vegetation_parameters == from_typology['vegetation_parameters']
    assert city.pavement_parameters == from_typology['pavement_parameters']
    assert city.traffic_parameters == from_typology['traffic_parameters']


def test_defaults(default):
    # TODO: Determine required defaults and add checks to make sure they are being
    # initialised properly
    pass
