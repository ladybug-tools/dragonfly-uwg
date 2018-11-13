from __future__ import division
import os

from dragonfly.uwg.run import RunManager
from dragonfly.district import District

from ladybug.analysisperiod import AnalysisPeriod

import pytest
from tests.fixtures.district import correct


def test_initialize(correct):
    relative_path = './tests/fixtures/epw/boston.epw'
    epw_path = os.path.abspath(relative_path)
    district = District(correct['typologies'],
                        correct['site_area'],
                        correct['climate_zone'],
                        correct['tree_coverage_ratio'],
                        correct['grass_coverage_ratio'],
                        correct['traffic_parameters'],
                        correct['vegetation_parameters'],
                        correct['pavement_parameters'],
                        correct['characteristic_length'])
    run_manager = RunManager(epw_path, district)

    assert run_manager.epw_file == epw_path
    assert run_manager.district.site_coverage_ratio == (20000.0 + 5000.0) / 90000
    assert run_manager.district.facade_to_site_ratio == (45000.0 + 15000.0) / 90000
    assert run_manager.district.bldg_type_ratios == {'Hospital,1980sPresent': 0.8,
                                                     'SmallOffice,NewConstruction': 0.2}
    assert run_manager.district.climate_zone == correct['climate_zone']
    assert run_manager.district.tree_coverage_ratio == correct['tree_coverage_ratio']
    assert run_manager.district.grass_coverage_ratio == correct['grass_coverage_ratio']
    assert run_manager.district.characteristic_length == 300.0
    assert run_manager.district.traffic_parameters == correct['traffic_parameters']
    assert run_manager.district.vegetation_parameters == correct['vegetation_parameters']
    assert run_manager.district.pavement_parameters == correct['pavement_parameters']


def test_save_uwg_file(correct):
    # set up the run manager
    epw_path = './tests/fixtures/epw/singapore.epw'
    district = District(correct['typologies'],
                        correct['site_area'],
                        correct['climate_zone'],
                        correct['tree_coverage_ratio'],
                        correct['grass_coverage_ratio'],
                        correct['traffic_parameters'],
                        correct['vegetation_parameters'],
                        correct['pavement_parameters'],
                        correct['characteristic_length'])
    run_manager = RunManager(epw_path, district)

    # save a uwg file
    saved_file = run_manager.save_uwg_file()
    assert os.path.isfile(saved_file)
    assert os.stat(saved_file).st_size > 1
    os.remove(saved_file)


def test_run_uwg(correct):
    # set up the run manager
    epw_path = './tests/fixtures/epw/boston.epw'
    district = District(correct['typologies'],
                        correct['site_area'],
                        correct['climate_zone'],
                        correct['tree_coverage_ratio'],
                        correct['grass_coverage_ratio'],
                        correct['traffic_parameters'],
                        correct['vegetation_parameters'],
                        correct['pavement_parameters'],
                        correct['characteristic_length'])
    a_period = AnalysisPeriod(1, 1, 0, 1, 7, 23)
    run_manager = RunManager(epw_path, district, analysis_period=a_period)

    # set the run manager to run through the uwg
    morphed_epw = run_manager.run()
    assert os.path.isfile(morphed_epw)
    assert os.stat(morphed_epw).st_size > 1
    os.remove(morphed_epw)


def test_json(correct):
    # set up the run manager
    epw_path = './tests/fixtures/epw/singapore.epw'
    district = District(correct['typologies'],
                        correct['site_area'],
                        correct['climate_zone'],
                        correct['tree_coverage_ratio'],
                        correct['grass_coverage_ratio'],
                        correct['traffic_parameters'],
                        correct['vegetation_parameters'],
                        correct['pavement_parameters'],
                        correct['characteristic_length'])
    run_manager = RunManager(epw_path, district)

    run_manager_json = run_manager.to_json()
    assert RunManager.from_json(run_manager_json).to_json() == run_manager_json
