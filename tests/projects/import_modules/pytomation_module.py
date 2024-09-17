import sys

from pytomation.action_metadata import action
from pytomation.module.manager import ModuleManager


@action()
def import_module_a_greetings(module_manager: ModuleManager):

    module_a = module_manager.import_module("module_a")

    sys.stderr.write(module_a.get_greetings())


@action()
def import_module_a_my_number(module_manager: ModuleManager):

    module_a = module_manager.import_module("module_a")

    sys.stderr.write(module_a.MY_NUMBER)


def from_root():
    return "Hello module"
