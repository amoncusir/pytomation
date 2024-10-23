from typing import Any, Generic, List, Optional, TypeVar

Node = TypeVar("Node", bound=Any)


class ReverseTree(Generic[Node]):

    parent: Optional[Node]
    children: List[Node]

    def __init__(self, parent: Optional[Node] = None):
        self.children = []
        self.set_parent(parent)

    @property
    def root(self) -> Node:
        parent = self.parent

        if parent is None:
            return self

        return parent.root

    def set_parent(self, parent: Optional[Node]):
        if parent is not None:
            parent.children.append(self)

        self.parent = parent

    def add_child(self, child: Node):
        if child is None:
            raise ValueError("Cannot add a None child")

        if child not in self.children:
            self.children.append(child)
            child.parent = self

    def get_all_parents(self) -> List[Node]:
        """
        Ordered list, starting from the most direct parent, until the tree root node.
        :return:
        """

        parents = []
        node = self

        while node.parent is not None:
            parent = node.parent
            parents.append(parent)
            node = parent

        return parents
