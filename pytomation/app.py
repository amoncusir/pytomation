import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List

from pytomation.action_inventory import ActionInventory
from pytomation.context import Context
from pytomation.errors import RunnerActionNotFoundError, RunnerModuleNotFoundError
from pytomation.module_graph import ModuleGraphBuilder
from pytomation.plugin import Plugin
from pytomation.profile import Profile

if TYPE_CHECKING:
    from pytomation.discovery import Discovery
    from pytomation.module import Module


# TODO: Useless principal app class. I can do it better...
class App:

    discovery: "Discovery"
    profiles: List[str]
    modules: Dict[str, "Module"]
    module_graph_builder: "ModuleGraphBuilder"
    args: List[str]
    plugins: List[Plugin]

    def __init__(self, discovery: "Discovery"):
        self.inventory = ActionInventory()
        self.module_graph_builder = ModuleGraphBuilder()
        self.discovery = discovery
        self.profiles = []
        self.modules = {}
        self.args = []
        self.plugins = []

    def build_context(self, module: "Module"):
        profile = Profile(self.profiles)
        plugins = {p.name: p for p in self.plugins}

        return Context(self, profile, self.args, module, plugins)

    def validate(self):

        logging.debug(f"Validating; modules={self.modules}; profiles={self.profiles}")

        if self.modules is None or len(self.modules) <= 0:
            raise ValueError("No modules specified")

        if self.profiles is None or len(self.profiles) <= 0:
            raise ValueError("No profiles specified")

    def find(self):
        if self.discovery is None:
            logging.error("discovery property must be defined")
            raise ValueError("No discovery specified")

        modules = self.discovery.find_modules()
        self.modules = self.module_graph_builder.build_graph(modules)

    def add_profile(self, profile: str):
        logging.debug(f"Adding profile: {profile}")

        if self.profiles is None:
            self.profiles = []

        self.profiles.append(profile)

    def add_profiles(self, profiles: List[str]):
        logging.debug(f"Adding profiles: {profiles}")

        if self.profiles is None:
            self.profiles = []

        self.profiles.extend(profiles)

    def add_args(self, args: List[str]):
        logging.debug(f"Adding args: {args}")

        self.args = args

    def add_plugin(self, name: str, builder: Callable[["Context"], Any]):
        logging.debug(f"Adding plugin: {name}")

        if self.plugins is None:
            self.plugins = []

        self.plugins.append(Plugin(name, builder))

    def load_module_branch(self, path: str) -> "Module":
        logging.debug(f"Loading module: <{path}>")

        self.validate()

        if path not in self.modules:
            logging.error(f"Module <{path}> not found")
            raise RunnerModuleNotFoundError(f"Module <{path}> not found")

        module = self.modules[path]

        if module is None:
            logging.error(f"Module <{path}> is not defined")
            raise RunnerModuleNotFoundError(path)

        if not module.is_executed:
            logging.debug(f"Loading module <{module.name}>")
            module.load()

        return module

    def run_action_on_module(self, dot_path: str, action: str, safe=True):
        logging.debug(f"Running action on module: <{dot_path}>")

        module = self.load_module_branch(dot_path)

        if action not in module:
            logging.error(f"Action <{action}> on module <{module.name}> not defined")
            raise RunnerActionNotFoundError(action, module)

        self.inventory.add_action(module, action, raise_error=safe)
        module.run_action(action, self.build_context(module))
