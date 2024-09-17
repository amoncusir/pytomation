import sys

from pytomation.action_metadata import action
from pytomation.module.manager import ModuleManager

MY_NUMBER = 3.14


def get_greetings():
    return "hello"


@action()
def module():
    sys.stderr.write("module_a")


@action()
def import_root_module(module_manager: ModuleManager):
    root = module_manager.import_module(ModuleManager.ROOT)

    sys.stderr.write(root.from_root())
