from pathlib import Path
from typing import Callable, Tuple

from pytomation.initializer.initializer import InitializationChain
from pytomation.initializer.types import RootPath
from pytomation.utils.chain import Chain, chain_process
from pytomation.utils.store import TypedStore


class RootPathStrategy(Chain):

    def process(self, next_chain: Callable[[TypedStore], None], context: TypedStore) -> Path:
        raise NotImplementedError("Implement this method")


class RootPathFinder(InitializationChain):

    strategy_chains: Tuple[RootPathStrategy, ...]

    def __init__(self, strategy: Tuple[RootPathStrategy, ...], order: int = 0):
        super().__init__(order)
        self.strategy_chains = strategy

    def process(self, next_handler: Callable[[TypedStore], TypedStore], context: TypedStore) -> TypedStore:

        root_path = chain_process(self.strategy_chains, context)

        if root_path is not None:
            context.put(root_path, type_value=RootPath)

        return next_handler(context)


class FileFindRootPath(RootPathStrategy):

    file_name: str

    def __init__(self, file_name: str):
        self.file_name = file_name

    def process(self, next_chain: Callable[[TypedStore], None], context: TypedStore):
        current_path = Path.cwd()
        back_paths = (current_path, *list(current_path.parents))

        for path in back_paths:
            if self._contains_file(path):
                return path

        next_chain(context)

    def _contains_file(self, pth: Path) -> bool:
        current_file = pth / self.file_name
        return current_file.is_file()


class CwdRootPath(RootPathStrategy):

    def process(self, next_chain: Callable[[TypedStore], None], context: TypedStore) -> Path:
        return Path.cwd()
