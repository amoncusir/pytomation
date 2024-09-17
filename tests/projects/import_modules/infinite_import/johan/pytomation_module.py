from pytomation.module.manager import ModuleManager

name = "Johan, The Module"


def from_viki_get_name_with_mine(module_manager: ModuleManager):
    viki = module_manager.import_module("infinite_import/viki")

    my_forgotten_name = viki.from_johan_get_name(module_manager)

    return f"{viki.name} - {my_forgotten_name}"
