![Dragonfly](https://www.ladybug.tools/assets/img/dragonfly.png)

[![Build Status](https://github.com/ladybug-tools/dragonfly-uwg/workflows/CI/badge.svg)](https://github.com/ladybug-tools/dragonfly-uwg/actions)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/dragonfly-uwg/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/dragonfly-uwg)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/) [![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)

# dragonfly-uwg

Dragonfly extension for urban heat island modeling.

Dragonfly-uwg uses the [Urban Weather Generator (uwg)](https://github.com/ladybug-tools/uwg) to morph EPW files to account for the [urban heat island effect](https://en.wikipedia.org/wiki/Urban_heat_island).

## Installation

`pip install -U dragonfly-uwg`

## QuickStart

```console
import dragonfly_uwg
```

## [API Documentation](http://ladybug-tools.github.io/dragonfly-uwg/docs)

## Local Development

1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/dragonfly-uwg

# or

git clone https://github.com/ladybug-tools/dragonfly-uwg
```
2. Install dependencies:
```
cd dragonfly-uwg
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytest tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./dragonfly_uwg
sphinx-build -b html ./docs ./docs/_build/docs
```
