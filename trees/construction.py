from random import shuffle

class Node:
    def __init__(self, left, val, right):
        self.left = left
        self.val = val
        self.right = right

    def __eq__(self, other):  # compares val, but not left or right
        return isinstance(other, Node) and self.val == other.val

    def __repr__(self):
        return '({}, {}, {})'.format(self.left, self.val, self.right)

def tuple_to_tree(x):
    if x is None:
        return None
    left, val, right = x
    return Node(tuple_to_tree(left), val, tuple_to_tree(right))  # recursive call

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
