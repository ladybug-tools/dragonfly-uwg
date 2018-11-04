from dragonfly.typology import Typology
from dragonfly.uwg.typologypar import TypologyPar
import pytest
from tests.fixtures.typology import correct, default


def test_initialise(correct):
    typology = Typology(correct['average_height'], correct['footprint_area'],
                        correct['facade_area'], correct['bldg_program'],
                        correct['bldg_age'], correct['floor_to_floor'],
                        correct['floor_area'], correct['glz_ratio'])

    assert typology.average_height == correct['average_height']
    assert typology.footprint_area == correct['footprint_area']
    assert typology.facade_area == correct['facade_area']
    assert typology.bldg_program == correct['bldg_program']
    assert typology.bldg_age == correct['bldg_age']
    assert typology.floor_to_floor == correct['floor_to_floor']
    assert typology.floor_area == correct['floor_area']
    assert typology.glz_ratio == correct['glz_ratio']


def test_defaults(default):
    typology = Typology(default['average_height'], default['footprint_area'],
                        default['facade_area'], default['bldg_program'],
                        default['bldg_age'])

    assert typology.floor_to_floor == default['floor_to_floor']
    assert typology.floor_area == default['floor_area']
    assert typology.glz_ratio == default['glz_ratio']
    assert typology.uwg_parameters == TypologyPar()

def test_merge_typologies():
    # TODO: Need to write tests for merge_typologies class method
    pass
