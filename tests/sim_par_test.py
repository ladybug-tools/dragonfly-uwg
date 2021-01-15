# coding=utf-8
from dragonfly_uwg.simulation.parameter import UWGSimulationParameter

from honeybee.altnumber import autocalculate

from tests.fixtures.sim_par import default_sim_par, custom_sim_par


def test_sim_par():
    """Test the existence of basic properties."""
    sim_par = default_sim_par()

    str(sim_par)  # test the string representation
    assert sim_par.climate_zone == autocalculate
    assert sim_par.timestep == 12


def test_duplicate():
    """Test the duplicate method."""
    sim_par = custom_sim_par()
    new_sim_par = sim_par.duplicate()
    assert new_sim_par is not sim_par

    assert new_sim_par.climate_zone == sim_par.climate_zone
    assert new_sim_par.timestep == sim_par.timestep


def test_to_from_dict():
    """Test the VegetationPararameter to_dict and from_dict methods."""
    sim_par = custom_sim_par()
    sim_par_dict = sim_par.to_dict()
    new_sim_par = UWGSimulationParameter.from_dict(sim_par_dict)

    assert new_sim_par.climate_zone == sim_par.climate_zone
    assert new_sim_par.timestep == sim_par.timestep
