import functools
from pathlib import Path
from typing import Callable, Dict, List, Optional, Self, Tuple

from pytomation.errors import ImmutableChangeError
from pytomation.module.action import Action


class Module:

    _name: str
    _docs: str
    _path: Path
    _actions: Dict[str, Action]
    _parent: Optional[Self]
    _children: Optional[List[Self]]
    _freeze: bool = False

    def __init__(
        self,
        name: str,
        docs: str,
        path: Path,
        actions: List[Action],
        parent: Optional[Self] = None,
        children: Optional[List[Self]] = None,
    ):

        self._name = name
        self._docs = docs
        self._path = path
        self._actions = {a.name: a for a in actions}
        self._children = children
        self._add_parent(parent)

    @property
    def name(self) -> str:
        return self._name

    @property
    def docs(self) -> str:
        return self._docs

    @property
    def path(self) -> Path:
        return self._path

    @functools.cached_property
    def actions(self) -> List[Action]:
        return list(self._actions.values())

    @property
    def root(self) -> Self:
        parent = self.parent

        if parent is None:
            return self

        return parent.root

    @property
    def parent(self) -> Optional[Self]:
        return self._parent

    @property
    def children(self) -> Optional[Tuple[Self]]:
        return tuple(self._children) if self._children is not None else None

    def _add_parent(self, parent: Self) -> None:
        if self._freeze:
            raise ImmutableChangeError()

        self._parent = parent
        if self._parent is not None:
            self._parent._add_child(self)

    def _add_child(self, child: Self) -> None:
        if self._freeze:
            raise ImmutableChangeError()

        if self._children is None:
            self._children = [child]
        else:
            self._children.append(child)

    def __getitem__(self, item):
        return self._actions[item]

    def __contains__(self, item):
        return item in self._actions.keys()

    def propagate_children_function(self, fn: Callable[[Self], None]):

        fn(self)

        if self.children is not None:
            for child in self.children:
                child.propagate_children_function(fn)

    def freeze(self):
        def freeze_fn(mod):
            mod._freeze = True

        self.propagate_children_function(freeze_fn)
