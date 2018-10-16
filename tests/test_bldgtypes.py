from dragonfly.bldgtypes import BuildingTypes
import pytest
from tests.fixtures.bldgtypes import readDOE_file_path


@pytest.mark.usefixtures("readDOE_file_path")
def test_imports_pickled_DOE_file(readDOE_file_path):
    building_types = BuildingTypes(readDOE_file_path)

    assert building_types is not None
