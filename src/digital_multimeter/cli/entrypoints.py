from digital_multimeter import __title__ as NAME, __version__ as VERSION
from digital_multimeter.cli import click
from digital_multimeter.exceptions import MultimeterException


def dmm():
    try:
        click.dmm()
    except MultimeterException as e:
        print("")
        print("{} v{}".format(NAME, VERSION))
        print("ERROR: ", end="")
        for err in iter(e.args):
            print(err)
        print("")
        exit(1)
