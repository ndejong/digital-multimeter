import logging
import sys
import warnings

import click

from digital_multimeter import __env_connect__ as ENV_CONNECT, __version__ as VERSION
from digital_multimeter.cli.config import Config
from digital_multimeter.exceptions import MultimeterException
from digital_multimeter.main import DigitalMultimeter
from digital_multimeter.utils import cli_output


@click.group()
@click.option("-q", "--quiet", is_flag=True, help="Quiet mode; priority over --verbose")
@click.option("-v", "--verbose", is_flag=True, help="Verbose logging; debug level.")
@click.option("-W", "--disable-warnings", is_flag=True, help="Disable Python warnings.")
@click.version_option(VERSION)
def dmm(quiet, verbose, disable_warnings):
    """
    Digital multimeter CLI tool utilizing the DigitalMultimeter() module.

    Configuration can be achieved through command arguments, environment values or config file.

    Documentation available https://digital-multimeter.readthedocs.io
    """

    if quiet:
        level = logging.CRITICAL
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format="[%(levelname)s|%(asctime)s|%(name)s]: %(message)s",
    )

    if not sys.warnoptions and not disable_warnings:
        warnings.simplefilter("default")


@dmm.command("read")
@click.option("-m", "--model", help="DMM model; overrides env-variable and config.", required=False, default="Default")
@click.option("-c", "--connect", help="DMM connection; overrides env-variable and config.", required=False)
@click.option("-C", "--config", help="Override config file; default=~/.digital-multimeter", required=False)
@click.option(
    "-n", "--count", type=int, help="Perform <count> readings; use 0 for non-stop.", required=False, default=1
)
@click.option("-o", "--output", help="Output target file; default=stdout", default="stdout", required=False)
@click.option("-f", "--format", help="Output format json/csv; default=json", default="json", required=False)
def get_reading(model, connect, config, count, output, format):
    """
    Read the digital multimeter and output data in various formats
    """
    configuration = Config(session_config_file=config)

    if configuration.model and (not model or model == "Default"):
        model = configuration.model

    if configuration.connect and not connect:
        connect = configuration.connect

    logger = logging.getLogger(__name__)
    logger.debug("model={}".format(model))
    logger.debug("connect={}".format(connect))

    if not connect:
        raise MultimeterException(
            "DigitalMultimeter --connect parameter not supplied.  See documentation to "
            "alternatively set this using the {} environment variable or using a configuration "
            "file.".format(ENV_CONNECT)
        )

    api = DigitalMultimeter(connect=connect, model=model)

    counted = 0
    while counted < count or count == 0:
        cli_output(api.get_reading(), format=format, output=output, count=counted)
        counted += 1
        logger.debug("Readings cycle count: {}".format(counted))


@dmm.command("models")
@click.option("-o", "--output", help="Output target file; default=stdout", default="stdout", required=False)
@click.option("-f", "--format", help="Output format json/csv; default=json", default="json", required=False)
def get_models_supported(output, format):
    """
    Provides a list of the supported digital multimeter models
    """
    cli_output(DigitalMultimeter().get_models_supported(), format=format, output=output)
