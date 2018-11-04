import pytest
from dragonfly.typology import Typology
from dragonfly.uwg.districtpar import VegetationPar, PavementPar, TrafficPar
from dragonfly.terrain import Terrain


@pytest.fixture
def correct():

    return {
        'average_bldg_height': 35.0,
        'site_coverage_ratio': 0.3,
        'facade_to_site_ratio': 4.0,
        'bldg_type_ratios': {
            'MidRiseApartment,Pre1980s': 0.7,
            'LargeOffice,1980sPresent': 0.3
        },
        'climate_zone': '5A',
        'tree_coverage_ratio': 0.3,
        'grass_coverage_ratio': 0.1,

        'traffic_parameters': TrafficPar(4),
        'vegetation_parameters': VegetationPar(),
        'pavement_parameters': PavementPar(),
        'characteristic_length': 400
    }


@pytest.fixture
def default():

    return {
        'average_bldg_height': 35.0,
        'site_coverage_ratio': 0.3,
        'facade_to_site_ratio': 4.0,
        'bldg_type_ratios': {
            'MidRiseApartment,Pre1980s': 0.7,
            'LargeOffice,1980sPresent': 0.3
        },
        'climate_zone': '5A',
        'tree_coverage_ratio': 0.,
        'grass_coverage_ratio': 0.,

        'traffic_parameters': TrafficPar(10),
        'vegetation_parameters': VegetationPar(),
        'pavement_parameters': PavementPar(),
        'characteristic_length': 500
    }


@pytest.fixture
def from_typology():
    typology1 = Typology(average_height=35.0,
                         footprint_area=45,
                         facade_area=33.0,
                         bldg_program='Hospital',
                         bldg_era='1980sPresent',
                         floor_to_floor=3.0)

    typology2 = Typology(average_height=35.0,
                         footprint_area=45.0,
                         facade_area=33.0,
                         bldg_program='SmallOffice',
                         bldg_era='NewConstruction',
                         floor_to_floor=3.0)

    terrain = Terrain(90000.0)

    return {
        'typologies': [typology1, typology2],
        'terrain': terrain,
        'climate_zone': '5A',
        'tree_coverage_ratio': 0.3,
        'grass_coverage_ratio': 0.1,
        'traffic_parameters': TrafficPar(4.0),
        'vegetation_parameters': VegetationPar(),
        'pavement_parameters': PavementPar(),
    }
