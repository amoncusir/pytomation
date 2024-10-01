from typing import Callable, List, Tuple

from pytomation.configuration import Configuration
from pytomation.configuration.factory import ConfigurationFactory
from pytomation.initializer.initializer import InitializationChain
from pytomation.utils.store import TypedStore


class ConfigurationInitializerChain(InitializationChain):

    factories: Tuple[ConfigurationFactory, ...]
    initial_configuration: Configuration

    def __init__(
        self, initial_configuration: Configuration, factories: Tuple[ConfigurationFactory, ...], order: int = 0
    ):
        super().__init__(order)
        self.initial_configuration = initial_configuration
        self.factories = factories

    def process(self, next_handler: Callable[[TypedStore], None], context: TypedStore):
        config = self._build_by_factories()

        context.put(config)

        next_handler(context)

    def _build_by_factories(self) -> Configuration:

        config = self.initial_configuration

        for factory in self.factories:
            config = factory.build(config)

        return config


class ConfigurationInitializerBuilder:

    factories: List[ConfigurationFactory]
    initial_configuration: Configuration

    def __init__(self):
        self.factories = []
        self.initial_configuration = Configuration()

    def add_factory(self, factory: ConfigurationFactory):
        self.factories.append(factory)

    def add_factories(self, *factories: ConfigurationFactory):
        self.factories.extend(factories)

    def build(self, chain_order: int) -> ConfigurationInitializerChain:
        return ConfigurationInitializerChain(self.initial_configuration, tuple(self.factories), chain_order)
