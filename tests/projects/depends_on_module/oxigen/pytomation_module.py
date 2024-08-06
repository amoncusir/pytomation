import sys

from pytomation.action_metadata import action


@action()
def molecule_o():
    sys.stderr.write("oxigen")
