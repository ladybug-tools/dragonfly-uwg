from dragonfly.uwg.typologypar import TypologyPar
from tests.fixtures.typology_parameters import default, correct
import pytest


def test_initialise(correct):
    typology_par = TypologyPar(
        correct['fract_heat_to_canyon'],
        correct['shgc'],
        correct['wall_albedo'],
        correct['roof_albedo'],
        correct['roof_veg_fraction']
    )

    assert typology_par.fract_heat_to_canyon == correct['fract_heat_to_canyon']
    assert typology_par.shgc == correct['shgc']
    assert typology_par.wall_albedo == correct['wall_albedo']
    assert typology_par.roof_albedo == correct['roof_albedo']
    assert typology_par.roof_veg_fraction == correct['roof_veg_fraction']


def test_defaults(default):
    typology_par = TypologyPar()

    assert typology_par.fract_heat_to_canyon == default['fract_heat_to_canyon']
    assert typology_par.shgc == default['shgc']
    assert typology_par.wall_albedo == default['wall_albedo']
    assert typology_par.roof_albedo == default['roof_albedo']
    assert typology_par.roof_veg_fraction == default['roof_veg_fraction']


def test_json(correct):
    typology_par = TypologyPar(
        correct['fract_heat_to_canyon'],
        correct['shgc'],
        correct['wall_albedo'],
        correct['roof_albedo'],
        correct['roof_veg_fraction']
    )

    param_json = typology_par.to_json()

    assert param_json == correct
    assert TypologyPar.from_json(param_json).to_json() == correct
