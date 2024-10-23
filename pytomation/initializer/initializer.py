from abc import abstractmethod
from typing import Callable, List

from pytomation.utils.chain import Chain, chain_process
from pytomation.utils.store import TypedStore


class InitializationChain(Chain):

    order: int

    def __init__(self, order=0):
        self.order = order

    @abstractmethod
    def process(self, next_handler: Callable[[TypedStore], TypedStore], context: TypedStore) -> TypedStore: ...


class InitializerHandler:

    chains: List[InitializationChain]

    def __init__(self, chains=None):
        if chains is None:
            chains = []

        self.chains = chains

    def add(self, chain: InitializationChain):
        self.chains.append(chain)

    def __call__(self):
        return chain_process(sorted(self.chains, key=lambda c: c.order), TypedStore())
