import pytest
from dragonfly.typology import Typology
from dragonfly.dfparameter import VegetationPar, PavementPar, TrafficPar
from dragonfly.terrain import Terrain


@pytest.fixture
def correct():

    return {
        'average_bldg_height': 35,
        'site_coverage_ratio': 0.3,
        'facade_to_site_ratio': 4,
        'bldg_type_ratios': {
            'MidRiseApartment,Pre1980s': 0.7,
            'LargeOffice,1980sPresent': 0.3
        },
        'climate_zone': '5A',
        'tree_coverage_ratio': 0.3,
        'grass_coverage_ratio': 0.1,
        'characteristic_length': 400,

        'vegetation_parameters': VegetationPar(),
        'pavement_parameters': PavementPar(),
        'traffic_parameters': TrafficPar(4),
    }


@pytest.fixture
def default():
    pass


@pytest.fixture
def from_typology():
    typology1 = Typology(average_height=35,
                         footprint_area=45,
                         facade_area=33,
                         bldg_program='Hospital',
                         bldg_age='1980sPresent',
                         floor_to_floor=3)

    typology2 = Typology(average_height=35,
                         footprint_area=45,
                         facade_area=33,
                         bldg_program='SmallOffice',
                         bldg_age='NewConstruction',
                         floor_to_floor=3)

    terrain = Terrain(300)

    return {
        'typologies': [typology1, typology2],
        'terrain': terrain,
        'climate_zone': '5A',
        'tree_coverage_ratio': 0.3,
        'grass_coverage_ratio': 0.1,
        'vegetation_parameters': VegetationPar(),
        'pavement_parameters': PavementPar(),
        'traffic_parameters': TrafficPar(4),
    }
