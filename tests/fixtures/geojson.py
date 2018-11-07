import pytest
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

single_polygon_path = os.path.join(dir_path,
                                   'geojson', 'singlePolygon.json')

single_polygon_with_hole_path = os.path.join(dir_path,
                                             'geojson', 'singlePolygonWithHoles.json')

single_polygon_array_path = os.path.join(dir_path,
                                         'geojson', 'singlePolygonArray.json')

multi_polygon_path = os.path.join(dir_path,
                                  'geojson', 'multiPolygon.json')


@pytest.fixture
def single_polygon():
    with open(single_polygon_path, 'r') as f:
        return json.loads(f.read())


@pytest.fixture
def single_polygon_with_hole():
    with open(single_polygon_with_hole_path, 'r') as f:
        return json.loads(f.read())


@pytest.fixture
def single_polygon_array():
    with open(single_polygon_array_path, 'r') as f:
        return json.loads(f.read())


@pytest.fixture
def multi_polygon():
    with open(multi_polygon_path, 'r') as f:
        return json.loads(f.read())
