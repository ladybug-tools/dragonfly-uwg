# coding=utf-8
import os
import sys

from ladybug.dt import Date

from dragonfly_uwg.run import run_uwg
from dragonfly_uwg.simulation.parameter import UWGSimulationParameter

from tests.fixtures.model import two_buildings


def test_run_uwg():
    """Test the running of a model through the UWG."""
    if (sys.version_info >= (3, 0)):
        model = two_buildings()

        uwg_par = UWGSimulationParameter()
        uwg_par.run_period.end_date = Date(1, 7)

        epw_path = './tests/epw/boston.epw'
        uwg_json, urban_epw = run_uwg(model, epw_path, uwg_par)
        
        assert os.path.isfile(uwg_json)
        assert os.path.isfile(urban_epw)
