import pytest
from click.testing import CliRunner
from digital_multimeter.cli import click
from digital_multimeter import __version__


def test_dmm_version():
    runner = CliRunner()
    result = runner.invoke(click.dmm, "--version")
    assert __version__ in result.output
    assert result.exit_code == 0


def test_dmm_help():
    runner = CliRunner()
    result = runner.invoke(click.dmm, "--help")
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
    assert result.exit_code == 0


def test_get_models_supported():
    runner = CliRunner()
    result = runner.invoke(click.get_models_supported)
    assert "models" in result.output
    assert "Default" in result.output
    assert result.exit_code == 0
