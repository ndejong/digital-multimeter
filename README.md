# Digital Multimeter
[![PyPi](https://img.shields.io/pypi/v/digital-multimeter.svg)](https://pypi.python.org/pypi/digital-multimeter/)
[![Build Status](https://api.travis-ci.org/ndejong/digital-multimeter.svg?branch=master)](https://travis-ci.org/ndejong/digital-multimeter/)

Digital Multimeter provides both a CLI interface and a Python3 library interface to receive data from a 
variety of digital multimeters.  Checkout the [list of supported multimeters](https://digital-multimeter.readthedocs.io/en/latest/docs/supported-multimeters).

## Project
* Github - [github.com/ndejong/digital-multimeter](https://github.com/ndejong/digital-multimeter)
* PyPI - [pypi.python.org/pypi/digital-multimeter](https://pypi.python.org/pypi/digital-multimeter/)
* TravisCI - [travis-ci.org/github/ndejong/digital-multimeter](https://travis-ci.org/github/ndejong/digital-multimeter)
* ReadTheDocs - [digital-multimeter.readthedocs.io](https://digital-multimeter.readthedocs.io/en/latest/)

## Installation
```shell
user@computer:~$ pip3 install digital-multimeter
```

## CLI Usage
Continuously read the digital-multimeter and pipe the JSON output through `jq` making it look prettier.
```shell
user@computer:~$ dmm read --count 0 | jq .
```

Plenty more command-line examples [available here](https://digital-multimeter.readthedocs.io/en/latest/docs/command-examples/).

## Python Module Usage
Python-module documentation is [available here](https://digital-multimeter.readthedocs.io/en/latest/docs/python3-module/).

## Change Log
Change log details are [available here](https://digital-multimeter.readthedocs.io/en/latest/docs/changelog/).

## To Do
* More tests

---
Copyright &copy; 2020 Nicholas de Jong
