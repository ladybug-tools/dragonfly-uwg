from __future__ import division

from dragonfly.district import District
from dragonfly.typology import Typology
from dragonfly.terrain import Terrain
import pytest
from tests.fixtures.district import correct, default, from_typology


def test_initialise(correct):
    district = District(
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

    assert district.average_bldg_height == correct['average_bldg_height']
    assert district.site_coverage_ratio == correct['site_coverage_ratio']
    assert district.facade_to_site_ratio == correct['facade_to_site_ratio']
    assert district.bldg_type_ratios == correct['bldg_type_ratios']
    assert district.climate_zone == correct['climate_zone']
    assert district.tree_coverage_ratio == correct['tree_coverage_ratio']
    assert district.grass_coverage_ratio == correct['grass_coverage_ratio']
    assert district.characteristic_length == correct['characteristic_length']
    assert district.vegetation_parameters == correct['vegetation_parameters']
    assert district.pavement_parameters == correct['pavement_parameters']
    assert district.traffic_parameters == correct['traffic_parameters']


def test_from_typologies(from_typology):
    district = District.from_typologies(typologies=from_typology['typologies'],
                                terrain=from_typology['terrain'],
                                climate_zone=from_typology['climate_zone'],
                                tree_coverage_ratio=from_typology['tree_coverage_ratio'],
                                grass_coverage_ratio=from_typology['grass_coverage_ratio'],
                                vegetation_parameters=from_typology['vegetation_parameters'],
                                pavement_parameters=from_typology['pavement_parameters'],
                                traffic_parameters=from_typology['traffic_parameters'])

    assert district.average_bldg_height == 35
    assert district.site_coverage_ratio == 45*2 / 300
    assert district.facade_to_site_ratio == 33*2 / 300
    assert district.bldg_type_ratios =={'Hospital,1980sPresent': 0.5,
                                    'SmallOffice,NewConstruction': 0.5}
    assert district.climate_zone == from_typology['climate_zone']
    assert district.tree_coverage_ratio == from_typology['tree_coverage_ratio']
    assert district.grass_coverage_ratio == from_typology['grass_coverage_ratio']
    # assert district.characteristic_length == 17.32 # TODO: Add proper check for this value
    assert district.vegetation_parameters == from_typology['vegetation_parameters']
    assert district.pavement_parameters == from_typology['pavement_parameters']
    assert district.traffic_parameters == from_typology['traffic_parameters']


def test_defaults(default):
    # TODO: Determine required defaults and add checks to make sure they are being
    # initialised properly
    pass
