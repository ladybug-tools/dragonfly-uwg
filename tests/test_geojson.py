from dragonfly.utilities import area_from_geojson
from tests.fixtures.geojson import single_polygon, single_polygon_with_hole,\
                                   single_polygon_array, multi_polygon
import pytest


def test_single_polygon(single_polygon):
    expected_area = single_polygon['features'][0]['properties']['area']
    area, perimeter = area_from_geojson(single_polygon)

    assert area > expected_area - 50
    assert area < expected_area + 50


def test_single_polygon_with_hole(single_polygon_with_hole):
    expected_area = single_polygon_with_hole['features'][0]['properties']['area']
    area, perimeter = area_from_geojson(single_polygon_with_hole)

    assert area > expected_area - 50
    assert area < expected_area + 50


def test_single_polygon_array(single_polygon_array, multi_polygon):
    expected_area = multi_polygon['features'][0]['properties']['area']
    area, perimeter = area_from_geojson(single_polygon_array)

    assert area > expected_area - 50
    assert area < expected_area + 50


def test_multi_polygon(multi_polygon):
    expected_area = multi_polygon['features'][0]['properties']['area']
    area, perimeter = area_from_geojson(multi_polygon)

    assert area > expected_area - 50
    assert area < expected_area + 50
