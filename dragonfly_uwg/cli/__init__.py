"""dragonfly-uwg commands which will be added to dragonfly command line interface."""
import click

from dragonfly.cli import main
from .simulate import simulate

# command group for all uwg extension commands.
@click.group(help='dragonfly uwg commands.')
def uwg():
    pass


# add sub-commands to uwg
uwg.add_command(simulate)

# add uwg sub-commands to dragonfly CLI
main.add_command(uwg)
