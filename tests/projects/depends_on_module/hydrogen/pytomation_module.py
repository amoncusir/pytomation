import sys

from pytomation.action_metadata import action
from pytomation.action_wrapper import depends_on


@action()
def molecule_h():
    sys.stderr.write("hydrogen")


@depends_on.run_before(":create_lab")
@depends_on.run_after(":add_heat")
@action()
def experiment():
    sys.stderr.write("hydrogen")
