from typing import Any, Generic, List, Optional, TypeVar

Node = TypeVar("Node", bound=Any)


class ReverseTree(Generic[Node]):

    parent: Optional[Node]
    children: List[Node]

    def __init__(self, parent: Optional[Node] = None):
        self.children = []
        self.set_parent(parent)

    def set_parent(self, parent: Node):
        if parent is not None:
            parent.children.append(self)

        self.parent = parent
