import sys

from pytomation.action_metadata import action
from pytomation.module.manager import ModuleManager

name = "Viki, The Module"


@action()
def import_johan_infinite_loop(module_manager: ModuleManager):

    johan = module_manager.import_module("infinite_import/johan")
    ours_names = johan.from_viki_get_name_with_mine(module_manager)

    sys.stderr.write(ours_names)


def from_johan_get_name(module_manager: ModuleManager):
    johan = module_manager.import_module("infinite_import/johan")
    return johan.name
