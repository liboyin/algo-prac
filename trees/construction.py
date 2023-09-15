from dataclasses import dataclass
from random import shuffle
from typing import Any, Generic, Optional

from comparable import T


@dataclass
class Node(Generic[T]):
    value: T
    left: Optional['Node[T]'] = None
    right: Optional['Node[T]'] = None

    @classmethod
    def from_tuple(cls, x: tuple | None) -> Optional['Node[T]']:  # 'Node[T]' | None is not allowed
        """
        Converts a tuple representation of a binary tree to a Node object.

        Args:
            x (tuple | None): `(value, left, right)`

        Returns:
            Node | None: The Node object representing the binary tree.
        """
        if x is None:
            return None
        value, left, right = x  # (value, left, right)
        return cls(value, cls.from_tuple(left), cls.from_tuple(right))  # recursive call

    def to_tuple(self) -> tuple | None:
        """
        Converts a Node object representing a binary tree to its tuple representation.

        Returns:
            tuple | None: `(value, left, right)`
        """
        result: list[tuple | T | None] = [self.value]
        result.append(None if self.left is None else self.left.to_tuple())  # recursive call
        result.append(None if self.right is None else self.right.to_tuple())  # recursive call
        return tuple(result)


def test_tuple_to_tree():
    assert Node.from_tuple(None) is None
    assert Node.from_tuple((1, None, None)) == Node(1, None, None)
    sample_in = (1, (2, None, None), (3, None, None))
    expected_out = Node(1, Node(2, None, None), Node(3, None, None))
    assert Node.from_tuple(sample_in) == expected_out


def test_tree_to_tuple():
    assert Node(1, None, None).to_tuple() == (1, None, None)
    sample_in = Node(1, Node(2, None, None), Node(3, None, None))
    expected_out = (1, (2, None, None), (3, None, None))
    assert sample_in.to_tuple() == expected_out


def random_bst(size: int) -> Node:
    """
    Generates a random binary search tree of the specified size.

    Args:
        size (int): The number of nodes in the binary search tree.

    Returns:
        Node: The root node of the generated binary search tree.

    Raises:
        AssertionError: If the size is less than or equal to 0.
    """
    assert size > 0, size
    xs = list(range(size))
    shuffle(xs)
    root = Node(xs[0], None, None)
    for x in xs[1:]:
        c = root
        while True:
            if x < c.value:
                if c.left is None:
                    c.left = Node(x, None, None)
                    break
                else:
                    c = c.left
            else:
                if c.right is None:
                    c.right = Node(x, None, None)
                    break
                else:
                    c = c.right
    return root
