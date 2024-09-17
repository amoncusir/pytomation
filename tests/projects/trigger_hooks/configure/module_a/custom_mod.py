import sys

from pytomation.action_metadata import action


@action()
def module():
    sys.stderr.write("module")
