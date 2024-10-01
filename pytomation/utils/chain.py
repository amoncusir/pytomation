from abc import abstractmethod
from functools import partial
from typing import Any, Callable, Iterable, Optional, TypeVar

ChainFn = TypeVar("ChainFn", bound=Callable[[Callable[[Any], Any], Any], Any])
ChainContext = TypeVar("ChainContext", bound=Any)


class Chain:

    @abstractmethod
    def process(self, next_chain: Callable[[ChainContext], Any], context: ChainContext) -> Any:
        raise NotImplementedError("Implement this method")

    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)


def chain_process(chains: Iterable[ChainFn], initial_ctx: Optional[ChainContext] = None) -> Optional[ChainContext]:

    iter_chains = iter(chains)

    def handler(context: ChainContext, chain: ChainFn):
        next_chain = next(iter_chains, lambda _, x: x)
        next_handler = partial(handler, chain=next_chain)

        return chain(next_handler, context)

    first_chain = next(iter_chains, None)

    if first_chain is not None:
        return handler(initial_ctx, first_chain)

    return initial_ctx
