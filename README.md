[![Build Status](https://travis-ci.org/ladybug-tools/dragonfly.svg?branch=master)](https://travis-ci.org/ladybug-tools/dragonfly)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/ladybug/badge.svg)](https://coveralls.io/github/ladybug-tools/ladybug)

[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)


# Dragonfly
![Screenshot](https://github.com/chriswmackey/Dragonfly/blob/master/dragonfly.png)

Dragonfly is a library to model, visualize, and analyze urban climate and energy energy use.

Dragonfly uses the [Urban Weather Generator (uwg)](https://github.com/ladybug-tools/urbanWeatherGen) and the [Ladybug core](https://github.com/ladybug-tools/ladybug)

## [API Documentation](http://www.ladybug.tools/apidoc/dragonfly/)

## UWG
To use the Urban Weather Generator (UWG) capabiites in dragonfly, you must install the following dependencies:
* ladybug - `pip install lbt-ladybug`
* uwg - `pip install uwg`

### Example
This example shows how to define building typologies and use them to morph a rural EPW to account for the urban conditions:

```
from dragonfly.typology import Typology
from dragonfly.uwg.districtpar import TrafficPar
from dragonfly.district import District
from dragonfly.uwg.run import RunManager

epw_path = 'C:\\ladybug\\USA_MA_Boston-Logan.Intl.AP.725090_TMY3\\USA_MA_Boston-Logan.Intl.AP.725090_TMY3.epw'

typology1 = Typology(average_height=50.0,
                     footprint_area=50000.0,
                     facade_area=200000.0,
                     bldg_program='LargeOffice',
                     bldg_era='1980sPresent',
                     floor_to_floor=4.0)
                     
typology2 = Typology(average_height=20.0,
                     footprint_area=20000.0,
                     facade_area=150000.0,
                     bldg_program='MidRiseApartment',
                     bldg_era='Pre1980s',
                     floor_to_floor=3.0)
                     
traffic = TrafficPar(10)

district = District(building_typologies=[typology1, typology2],
                    site_area=150000.0,
                    climate_zone='5A',
                    traffic_parameters=traffic)

rm = RunManager(epw_path, district)
rm.run()
```
