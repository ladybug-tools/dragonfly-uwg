from dragonfly.uwg.districtpar import TrafficPar
import pytest
from tests.fixtures.traffic_parameter import correct, incorrect, default


def test_initialise(correct):
    correct_parameters = TrafficPar(correct['sensible_heat'],
                                    correct['weekday_schedule'],
                                    correct['saturday_schedule'],
                                    correct['sunday_schedule'])

    assert correct_parameters.sensible_heat == correct['sensible_heat']
    assert correct_parameters.weekday_schedule == correct['weekday_schedule']
    assert correct_parameters.saturday_schedule == correct['saturday_schedule']
    assert correct_parameters.sunday_schedule == correct['sunday_schedule']


def test_error_handling(correct, incorrect):
    with pytest.raises(AssertionError,
                       match='sensible_heat must be a number got *'):
        TrafficPar(incorrect['sensible_heat'],
                   correct['weekday_schedule'],
                   correct['saturday_schedule'],
                   correct['sunday_schedule'])

    with pytest.raises(ValueError,
                       match='schedule value must be between 0 and 1. Current value is *'):
        TrafficPar(correct['sensible_heat'],
                   incorrect['non_fractional'],
                   correct['saturday_schedule'],
                   correct['sunday_schedule'])

    with pytest.raises(Exception,
                       match='Current schedule has length \d*. Daily schedules must be lists of 24 values'):
        TrafficPar(correct['sensible_heat'],
                   correct['weekday_schedule'],
                   incorrect['too_short'],
                   correct['sunday_schedule'])

    with pytest.raises(Exception,
                       match='Current schedule has length \d*. Daily schedules must be lists of 24 values'):
        TrafficPar(correct['sensible_heat'],
                   correct['weekday_schedule'],
                   incorrect['too_long'],
                   correct['sunday_schedule'])


def test_default(default):
    default_parameters = TrafficPar(4)

    assert default_parameters.weekday_schedule == default['weekday_schedule']
    assert default_parameters.saturday_schedule == default['saturday_schedule']
    assert default_parameters.sunday_schedule == default['sunday_schedule']


def test_json(correct):
    parameters = TrafficPar(correct['sensible_heat'],
                            correct['weekday_schedule'],
                            correct['saturday_schedule'],
                            correct['sunday_schedule'])

    param_json = parameters.to_json()

    assert param_json == correct
    assert TrafficPar.from_json(param_json).to_json() == correct
