from abc import abstractmethod
from functools import partial
from typing import Callable, List

from pytomation.utils.store import TypedStore


class InitializationChain:

    order: int

    def __init__(self, order=0):
        self.order = order

    @abstractmethod
    def handle(self, next_handler: Callable[[TypedStore], None], context: TypedStore):
        raise NotImplementedError("Implement this method")


class InitializerHandler:

    chains: List[InitializationChain]

    def __init__(self, chains=None):
        if chains is None:
            chains = []

        self.chains = chains

    def add(self, chain: InitializationChain):
        self.chains.append(chain)

    def __call__(self):

        last_chain = _LastChain()

        iter_chains = iter(sorted(self.chains, key=lambda c: c.order))

        def process_handler(context, handler: InitializationChain):

            last_chain.context = context
            next_chain = next(iter_chains, last_chain)
            next_handler = partial(process_handler, handler=next_chain)

            handler.handle(next_handler, context)

        process_handler(TypedStore(), next(iter_chains, None))

        return last_chain.context


class _LastChain(InitializationChain):

    context: TypedStore

    def handle(self, _: None, context: TypedStore):
        self.context = context
