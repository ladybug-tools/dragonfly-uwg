"""Test cli simulate module."""
from click.testing import CliRunner
from dragonfly_uwg.cli.simulate import simulate_model
from ladybug.config import folders
from ladybug.futil import nukedir

import os
import sys


def test_simulate_idf():
    if (sys.version_info >= (3, 0)):
        runner = CliRunner()
        input_model = './tests/json/model_complete_simple.dfjson'
        input_epw = './tests/epw/singapore.epw'
        input_sim_par = './tests/json/uwg_sim_par.json'

        result = runner.invoke(
            simulate_model, [input_model, input_epw, '--sim-par-json', input_sim_par])
        assert result.exit_code == 0

        epw_dir = os.path.join(folders.default_epw_folder, 'NewDevelopment')
        output_json = os.path.join(epw_dir, 'NewDevelopment_uwg.json')
        output_epw = os.path.join(epw_dir, 'NewDevelopment.epw')
        assert os.path.isfile(output_json)
        assert os.path.isfile(output_epw)
        nukedir(epw_dir)
