import sys

from pytomation.action_metadata import action


@action()
def root():
    sys.stderr.write("root")
