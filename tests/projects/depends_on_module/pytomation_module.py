import sys

from pytomation.action_metadata import action
from pytomation.action_wrapper import depends_on


@action()
@depends_on.run_before("hydrogen:molecule_h")
@depends_on.run_before("oxigen:molecule_o")
def create_water():
    sys.stderr.write("=water")


@action()
def create_lab():
    sys.stderr.write("lab-")


@action()
def add_heat():
    sys.stderr.write("-explosion")
