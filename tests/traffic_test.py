# coding=utf-8
from dragonfly_uwg.traffic import TrafficParameter

from honeybee.altnumber import autocalculate

from tests.fixtures.traffic import default_traffic, custom_traffic


def test_traffic():
    """Test the existence of basic properties."""
    traffic = default_traffic()

    str(traffic)  # test the string representation
    assert traffic.watts_per_area == autocalculate
    assert traffic.weekday_schedule == TrafficParameter.WEEKDAY_DEFAULT
    assert traffic.saturday_schedule == TrafficParameter.SATURDAY_DEFAULT
    assert traffic.sunday_schedule == TrafficParameter.SUNDAY_DEFAULT


def test_duplicate():
    """Test the duplicate method."""
    traffic = custom_traffic()
    new_traffic = traffic.duplicate()
    assert new_traffic is not traffic

    assert new_traffic.watts_per_area == traffic.watts_per_area
    assert new_traffic.weekday_schedule == traffic.weekday_schedule
    assert new_traffic.saturday_schedule == traffic.saturday_schedule
    assert new_traffic.sunday_schedule == traffic.sunday_schedule


def test_to_from_dict():
    """Test the TrafficParameter to_dict and from_dict methods."""
    traffic = custom_traffic()
    traffic_dict = traffic.to_dict()
    new_traffic = TrafficParameter.from_dict(traffic_dict)

    assert new_traffic.watts_per_area == traffic.watts_per_area
    assert new_traffic.weekday_schedule == traffic.weekday_schedule
    assert new_traffic.saturday_schedule == traffic.saturday_schedule
    assert new_traffic.sunday_schedule == traffic.sunday_schedule
    assert new_traffic.to_dict() == traffic_dict
