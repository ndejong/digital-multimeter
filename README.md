# Digital Multimeter
[![PyPi](https://img.shields.io/pypi/v/digital-multimeter.svg)](https://pypi.python.org/pypi/digital-multimeter/)
[![Python Versions](https://img.shields.io/pypi/pyversions/digital-multimeter.svg)](https://github.com/ndejong/digital-multimeter/)
[![Build Status](https://api.travis-ci.org/ndejong/digital-multimeter.svg?branch=master)](https://travis-ci.org/ndejong/digital-multimeter/)
![Read the Docs](https://img.shields.io/readthedocs/digital-multimeter)
![PyPI license](https://img.shields.io/pypi/l/digital-multimeter.svg)

Digital Multimeter provides both a command-line interface and a Python module interface to receive data from a 
variety of digital multimeters.  Checkout the [list of supported multimeters](https://digital-multimeter.readthedocs.io/en/latest/docs/supported-multimeters).

## Features
* Command line and Python module interface to digital multimeters
* Continuous live data readings (using `--count 0`)
* Output in **json** or **csv** formats
* Output to console or file, allowing other tools to pickup and use the data
* Configuration via config-file or environment-variables
* Easy to expand for new digital-multimeter protocols
* Easy installation using PyPI `pip`
* Plenty of documentation and examples - https://digital-multimeter.readthedocs.io

## Installation
```shell
user@computer:~$ pip3 install digital-multimeter
```

## Command Line Usage
Continuously read the digital-multimeter and pipe the JSON output through `jq` making it look prettier.
```shell
user@computer:~$ dmm read --connect /dev/ttyUSB0 --count 0 | jq .
{
  "reading": {
    "value": 156.70000000000002,
    "unit_name": "volts",
    "unit_symbol": "V",
    "scale": 0.001,
    "scale_name": "milli",
    "scale_symbol": "m",
    "scaled_value": 0.15670000000000003,
    "is_relative": false
  },
  "instrument": {
    "module": "MultimeterDigitechQM1538",
    "operation_mode": "voltage_dc",
    "low_battery": false,
    "is_hold": false
  },
  "time": {
    "elapsed": 0.349347334,
    "interval": 0.349347334,
    "timestamp": 1605936374.7694516,
    "unit_name": "second",
    "unit_symbol": "s"
  }
}
```

Plenty more command-line examples [available here](https://digital-multimeter.readthedocs.io/en/latest/docs/command-examples/).

## Python Module Usage
Python-module documentation is [available here](https://digital-multimeter.readthedocs.io/en/latest/docs/python3-module/).

## Project
* Github - [github.com/ndejong/digital-multimeter](https://github.com/ndejong/digital-multimeter)
* PyPI - [pypi.python.org/pypi/digital-multimeter](https://pypi.python.org/pypi/digital-multimeter/)
* TravisCI - [travis-ci.org/github/ndejong/digital-multimeter](https://travis-ci.org/github/ndejong/digital-multimeter)
* ReadTheDocs - [digital-multimeter.readthedocs.io](https://digital-multimeter.readthedocs.io/en/latest/)

---
Copyright &copy; 2020 Nicholas de Jong
