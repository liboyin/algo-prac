from dataclasses import dataclass
from random import shuffle

from comparable import T


@dataclass
class Node:
    value: T
    left: 'Node' = None
    right: 'Node' = None


def tuple_to_tree(x):
    if x is None:
        return None
    return Node(tuple_to_tree(x.left), x.val, tuple_to_tree(x.right))  # recursive call


def tree_to_tuple(x):
    if x is None:
        return None
    return (tree_to_tuple(x.left), x.val, tree_to_tuple(x.right))  # recursive call


def random_bst(size):
    assert size > 0
    xs = list(range(size))
    shuffle(xs)
    root = Node(None, xs[0], None)
    for x in xs[1:]:
        c = root
        while True:
            if x < c.val:
                if c.left is None:
                    c.left = Node(None, x, None)
                    break
                else:
                    c = c.left
            else:
                if c.right is None:
                    c.right = Node(None, x, None)
                    break
                else:
                    c = c.right
    return root
