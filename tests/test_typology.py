from dragonfly.typology import Typology
from dragonfly.uwg.typologypar import TypologyPar
from tests.fixtures.typology import default, correct
from tests.fixtures.typology_parameters import correct as uwg_params
import pytest


def test_initialise(correct):
    typology = Typology(correct['average_height'], correct['footprint_area'],
                        correct['facade_area'], correct['bldg_program'],
                        correct['bldg_era'], correct['floor_to_floor'],
                        correct['floor_area'], correct['glz_ratio'])

    assert typology.average_height == correct['average_height']
    assert typology.footprint_area == correct['footprint_area']
    assert typology.facade_area == correct['facade_area']
    assert typology.bldg_program == correct['bldg_program']
    assert typology.bldg_era == correct['bldg_era']
    assert typology.floor_to_floor == correct['floor_to_floor']
    assert typology.floor_area == correct['floor_area']
    assert typology.glz_ratio == correct['glz_ratio']


def test_defaults(default):
    typology = Typology(default['average_height'], default['footprint_area'],
                        default['facade_area'], default['bldg_program'],
                        default['bldg_era'])

    assert typology.floor_to_floor == default['floor_to_floor']
    assert typology.floor_area == default['floor_area']
    assert typology.glz_ratio == default['glz_ratio']
    assert typology.uwg_parameters.fract_heat_to_canyon == 0.5


def test_merge_typologies():
    # TODO: Need to write tests for merge_typologies class method
    pass


def test_json(correct, uwg_params):
    uwg_par = TypologyPar(
        uwg_params['fract_heat_to_canyon'],
        uwg_params['shgc'],
        uwg_params['wall_albedo'],
        uwg_params['roof_albedo'],
        uwg_params['roof_veg_fraction']
    )

    typology = Typology(correct['average_height'], correct['footprint_area'],
                        correct['facade_area'], correct['bldg_program'],
                        correct['bldg_era'], correct['floor_to_floor'],
                        correct['floor_area'], correct['glz_ratio'],
                        uwg_par)

    typology_json = typology.to_json()
    correct['uwg_parameters'] = uwg_par.to_json()

    assert typology_json == correct
    assert Typology.from_json(typology_json).to_json() == correct
