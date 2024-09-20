from abc import abstractmethod
from functools import partial
from typing import Any, Callable, Iterable, Optional, TypeVar

from tests.unittest.utils import pass_fn

ChainFn = TypeVar("ChainFn", bound=Callable[[Callable[[Any], None], Any], None])
ChainContext = TypeVar("ChainContext", bound=Any)


class Chain:

    @abstractmethod
    def process(self, next_chain: Callable[[ChainContext], None], context: ChainContext):
        raise NotImplementedError("Implement this method")

    def __call__(self, *args, **kwargs):
        self.process(*args, **kwargs)


def chain_process(chains: Iterable[ChainFn], initial_ctx: Optional[ChainContext] = None) -> Optional[ChainContext]:

    iter_chains = iter(chains)
    through_context = initial_ctx

    def handler(context: ChainContext, chain: ChainFn):
        nonlocal through_context

        through_context = context
        next_chain = next(iter_chains, pass_fn)
        next_handler = partial(handler, chain=next_chain)

        chain(next_handler, context)

    first_chain = next(iter_chains, None)

    if first_chain is not None:
        handler(through_context, first_chain)

    return through_context


def sequential(
    chains: Iterable[Callable[..., Any]],
    pass_ctx: Callable[[Callable[..., Any], ChainContext], ChainContext],
    initial_ctx: ChainContext = None,
) -> ChainContext:
    ctx = initial_ctx

    for chain in chains:
        ctx = pass_ctx(chain, ctx)

    return ctx
