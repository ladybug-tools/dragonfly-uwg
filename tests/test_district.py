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
        traffic_parameters=correct['traffic_parameters'],
        vegetation_parameters=correct['vegetation_parameters'],
        pavement_parameters=correct['pavement_parameters'],
        characteristic_length=correct['characteristic_length']
    )

    assert district.average_bldg_height == correct['average_bldg_height']
    assert district.site_coverage_ratio == correct['site_coverage_ratio']
    assert district.facade_to_site_ratio == correct['facade_to_site_ratio']
    assert district.bldg_type_ratios == correct['bldg_type_ratios']
    assert district.climate_zone == correct['climate_zone']
    assert district.tree_coverage_ratio == correct['tree_coverage_ratio']
    assert district.grass_coverage_ratio == correct['grass_coverage_ratio']
    assert district.traffic_parameters == correct['traffic_parameters']
    assert district.vegetation_parameters == correct['vegetation_parameters']
    assert district.pavement_parameters == correct['pavement_parameters']
    assert district.characteristic_length == correct['characteristic_length']


def test_from_typologies(from_typology):
    district = District.from_typologies(from_typology['typologies'],
                                        from_typology['terrain'],
                                        from_typology['climate_zone'],
                                        from_typology['tree_coverage_ratio'],
                                        from_typology['grass_coverage_ratio'],
                                        from_typology['traffic_parameters'],
                                        from_typology['vegetation_parameters'],
                                        from_typology['pavement_parameters'])

    assert district.average_bldg_height == 35
    assert district.site_coverage_ratio == (45 * 2) / 90000
    assert district.facade_to_site_ratio == (33 * 2) / 90000
    assert district.bldg_type_ratios == {'Hospital,1980sPresent': 0.5,
                                         'SmallOffice,NewConstruction': 0.5}
    assert district.climate_zone == from_typology['climate_zone']
    assert district.tree_coverage_ratio == from_typology['tree_coverage_ratio']
    assert district.grass_coverage_ratio == from_typology['grass_coverage_ratio']
    assert district.characteristic_length == 300
    assert district.traffic_parameters == from_typology['traffic_parameters']
    assert district.vegetation_parameters == from_typology['vegetation_parameters']
    assert district.pavement_parameters == from_typology['pavement_parameters']


def test_defaults(default):
    district = District(
        average_bldg_height=default['average_bldg_height'],
        site_coverage_ratio=default['site_coverage_ratio'],
        facade_to_site_ratio=default['facade_to_site_ratio'],
        bldg_type_ratios=default['bldg_type_ratios'],
        climate_zone=default['climate_zone']
    )

    assert district.average_bldg_height == default['average_bldg_height']
    assert district.site_coverage_ratio == default['site_coverage_ratio']
    assert district.facade_to_site_ratio == default['facade_to_site_ratio']
    assert district.bldg_type_ratios == default['bldg_type_ratios']
    assert district.climate_zone == default['climate_zone']
    assert district.tree_coverage_ratio == default['tree_coverage_ratio']
    assert district.grass_coverage_ratio == default['grass_coverage_ratio']
    assert district.traffic_parameters.sensible_heat == \
        default['traffic_parameters'].sensible_heat
    assert district.characteristic_length == correct['characteristic_length']
