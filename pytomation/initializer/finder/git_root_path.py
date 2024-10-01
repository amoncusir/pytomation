from pathlib import Path
from typing import TYPE_CHECKING, Callable

import git

from pytomation.initializer.finder.root_path import RootPathStrategy

if TYPE_CHECKING:
    from pytomation.utils.store import TypedStore


class GitRootPath(RootPathStrategy):

    def process(self, next_chain: Callable[[TypedStore], Path], context: TypedStore) -> Path:

        try:
            repo = git.Repo(Path.cwd(), search_parent_directories=True)
            return repo.git.rev_parse("--show-toplevel")

        except git.exc.InvalidGitRepositoryError:
            return next_chain(context)
