# coding=utf-8
from dragonfly.properties import ModelProperties, BuildingProperties, StoryProperties, \
    Room2DProperties, ContextShadeProperties
import dragonfly.writer.model as model_writer

from .properties.model import ModelUWGProperties
from .properties.building import BuildingUWGProperties
from .properties.story import StoryUWGProperties
from .properties.room2d import Room2DUWGProperties
from .properties.context import ContextShadeUWGProperties
from .writer import model_to_uwg


# set a hidden uwg attribute on each core geometry Property class to None
# define methods to produce uwg property instances on each Property instance
ModelProperties._uwg = None
BuildingProperties._uwg = None
StoryProperties._uwg = None
Room2DProperties._uwg = None
ContextShadeProperties._uwg = None


def model_uwg_properties(self):
    if self._uwg is None:
        self._uwg = ModelUWGProperties(self.host)
    return self._uwg


def building_uwg_properties(self):
    if self._uwg is None:
        self._uwg = BuildingUWGProperties(self.host)
    return self._uwg


def story_uwg_properties(self):
    if self._uwg is None:
        self._uwg = StoryUWGProperties(self.host)
    return self._uwg


def room2d_uwg_properties(self):
    if self._uwg is None:
        self._uwg = Room2DUWGProperties(self.host)
    return self._uwg


def context_uwg_properties(self):
    if self._uwg is None:
        self._uwg = ContextShadeUWGProperties(self.host)
    return self._uwg


# add uwg property methods to the Properties classes
ModelProperties.uwg = property(model_uwg_properties)
BuildingProperties.uwg = property(building_uwg_properties)
StoryProperties.uwg = property(story_uwg_properties)
Room2DProperties.uwg = property(room2d_uwg_properties)
ContextShadeProperties.uwg = property(context_uwg_properties)

# add model writer to uwg
model_writer.uwg = model_to_uwg
