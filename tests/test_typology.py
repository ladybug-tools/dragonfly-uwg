from dragonfly.typology import Typology
import pytest
from tests.fixtures.typology import correct, default


def test_initialise(correct):
    typology = Typology(correct['average_height'], correct['footprint_area'],
                        correct['facade_area'], correct['bldg_program'],
                        correct['bldg_age'], correct['floor_to_floor'],
                        correct['fract_heat_to_canyon'], correct['glz_ratio'],
                        correct['floor_area'])

    assert typology.average_height == correct['average_height']
    assert typology.footprint_area == correct['footprint_area']
    assert typology.facade_area == correct['facade_area']
    assert typology.bldg_program == correct['bldg_program']
    assert typology.bldg_age == correct['bldg_age']
    assert typology.floor_to_floor == correct['floor_to_floor']
    assert typology.fract_heat_to_canyon == correct['fract_heat_to_canyon']
    assert typology.glz_ratio == correct['glz_ratio']
    assert typology.floor_area == correct['floor_area']


def test_defaults(default):
    # TODO: Determine required defaults and add checks to make sure they are being
    # initialised properly
    pass


def test_merge_typologies():
    # TODO: Need to write tests for merge_typologies class method
    pass
