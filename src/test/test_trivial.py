
import pytest
from digital_multimeter import __author__
from digital_multimeter import __version__
from digital_multimeter import __title__
from digital_multimeter import __license__


def test_author_exist():
    assert __author__ is not None


def test_version_exist():
    assert __version__ is not None


def test_title_exist():
    assert __title__ is not None


def test_license_exist():
    assert __license__ is not None
