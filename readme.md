# Digital Multimeter
[![PyPi](https://img.shields.io/pypi/v/digital-multimeter.svg)](https://pypi.python.org/pypi/digital-multimeter/)
[![Python Versions](https://img.shields.io/pypi/pyversions/digital-multimeter.svg)](https://github.com/ndejong/digital-multimeter/)
[![Read the Docs](https://img.shields.io/readthedocs/digital-multimeter)](https://digital-multimeter.readthedocs.io)
![License](https://img.shields.io/github/license/ndejong/digital-multimeter.svg)

Digital Multimeter provides both a CLI and Python API interface to receive data 
from a variety of digital multimeters.  

See the list of supported multimeters [here](https://digital-multimeter.readthedocs.io/en/latest/supported-multimeters/).

## Features
* Command line and Python module interface to digital multimeters
* Continuous live data readings (using `--count 0`)
* Output in **json** or **csv** formats
* Output to console or file, allowing other tools to pickup and use the data
* Configuration via config-file or environment-variables
* Easy to expand for new digital-multimeter protocols
* Easy installation using PyPI `pip`
* Documentation and examples at [digital-multimeter.readthedocs.io](https://digital-multimeter.readthedocs.io)

## Installation
```shell
user@computer:~$ pip install [--upgrade] digital-multimeter
```

## CLI Usage Example
Continuously read the digital-multimeter and pipe the JSON output through `jq` to 
make the JSON output look prettier.
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

## Python API Usage
Python-module documentation is available [here](https://digital-multimeter.readthedocs.io/en/latest/api/digitalmultimeter/).

## Project
* Github - [github.com/ndejong/digital-multimeter](https://github.com/ndejong/digital-multimeter)
* PyPI - [pypi.python.org/pypi/digital-multimeter](https://pypi.python.org/pypi/digital-multimeter/)
* ReadTheDocs - [digital-multimeter.readthedocs.io](https://digital-multimeter.readthedocs.io)

---
Copyright &copy; 2021-2023 [Nicholas de Jong](https://www.nicholasdejong.com)
