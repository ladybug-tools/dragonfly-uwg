from __future__ import division

from dragonfly.district import District
import pytest
from tests.fixtures.district import correct, default, from_geo_params


def test_initialize(correct):
    district = District(correct['typologies'],
                        correct['site_area'],
                        correct['climate_zone'],
                        correct['tree_coverage_ratio'],
                        correct['grass_coverage_ratio'],
                        correct['traffic_parameters'],
                        correct['vegetation_parameters'],
                        correct['pavement_parameters'],
                        correct['characteristic_length'])

    assert district.average_bldg_height == 35
    assert district.site_coverage_ratio == (20000.0 + 5000.0) / 90000
    assert district.facade_to_site_ratio == (45000.0 + 15000.0) / 90000
    assert district.bldg_type_ratios == {'Hospital,1980sPresent': 0.8,
                                         'SmallOffice,NewConstruction': 0.2}
    assert district.climate_zone == correct['climate_zone']
    assert district.tree_coverage_ratio == correct['tree_coverage_ratio']
    assert district.grass_coverage_ratio == correct['grass_coverage_ratio']
    assert district.characteristic_length == 300.0
    assert district.traffic_parameters == correct['traffic_parameters']
    assert district.vegetation_parameters == correct['vegetation_parameters']
    assert district.pavement_parameters == correct['pavement_parameters']


def test_from_geo_params(from_geo_params):
    district = District.from_geo_params(
        average_bldg_height=from_geo_params['average_bldg_height'],
        site_coverage_ratio=from_geo_params['site_coverage_ratio'],
        facade_to_site_ratio=from_geo_params['facade_to_site_ratio'],
        bldg_type_ratios=from_geo_params['bldg_type_ratios'],
        climate_zone=from_geo_params['climate_zone'],
        tree_coverage_ratio=from_geo_params['tree_coverage_ratio'],
        grass_coverage_ratio=from_geo_params['grass_coverage_ratio'],
        traffic_parameters=from_geo_params['traffic_parameters'],
        vegetation_parameters=from_geo_params['vegetation_parameters'],
        pavement_parameters=from_geo_params['pavement_parameters'],
        characteristic_length=from_geo_params['characteristic_length']
    )

    assert district.average_bldg_height == from_geo_params['average_bldg_height']
    assert district.site_coverage_ratio == from_geo_params['site_coverage_ratio']
    assert district.facade_to_site_ratio == from_geo_params['facade_to_site_ratio']
    assert district.bldg_type_ratios == from_geo_params['bldg_type_ratios']
    assert district.climate_zone == from_geo_params['climate_zone']
    assert district.tree_coverage_ratio == from_geo_params['tree_coverage_ratio']
    assert district.grass_coverage_ratio == from_geo_params['grass_coverage_ratio']
    assert district.traffic_parameters == from_geo_params['traffic_parameters']
    assert district.vegetation_parameters == from_geo_params['vegetation_parameters']
    assert district.pavement_parameters == from_geo_params['pavement_parameters']
    assert district.characteristic_length == from_geo_params['characteristic_length']


def test_from_geo_params_default(default):
    district = District.from_geo_params(
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


def test_json(correct):
    district = District(correct['typologies'],
                        correct['site_area'],
                        correct['climate_zone'],
                        correct['tree_coverage_ratio'],
                        correct['grass_coverage_ratio'],
                        correct['traffic_parameters'],
                        correct['vegetation_parameters'],
                        correct['pavement_parameters'],
                        correct['characteristic_length'])

    district_json = district.to_json()
    assert District.from_json(district_json).to_json() == district_json
