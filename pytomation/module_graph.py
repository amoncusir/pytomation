from typing import Sequence, Dict

from pytomation.module import Module

MODULE_PATH_SPLITTER = "/"


def find_near_parent(
    dict_modules: Dict[str, Module], path: Sequence[str]
) -> Module:
    len_path = len(path)

    for node in reversed(range(len_path)):
        dot_path = MODULE_PATH_SPLITTER.join(path[:node])

        if dot_path in dict_modules:
            return dict_modules[dot_path]


class ModuleGraphBuilder:

    def __init__(self, module_path_splitter=MODULE_PATH_SPLITTER):
        self.module_path_splitter = module_path_splitter

    def build_graph(self, modules: Sequence[Module]) -> Dict[str, Module]:
        kv_module = {m.name: m for m in modules}
        without_root = filter(lambda m: m.name != "", modules)

        for module in without_root:
            nodes_path = module.name.split(self.module_path_splitter)
            parent = find_near_parent(kv_module, nodes_path)
            parent.append_child(module)
            module.parent = parent

        return kv_module
