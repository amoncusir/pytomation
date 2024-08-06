import sys

from pytomation.action_metadata import action


@action()
def spread_action():
    send_echo_test()


@action()
def banana():
    send_echo_test()


def send_echo_test():
    sys.stderr.write("banana")
