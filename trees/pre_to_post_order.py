from math import inf
from trees.construction import Node
from trees.traversal import rec_free_post_order

def convert(seq):
    """
    Converts a pre-order traversal sequence of a valid binary search tree to a post-order traversal sequence. Assumes
        unique elements. An invalid pre-order traversal sequence triggers an AssertionError.
    Solution is a combination of pre-order verification, pre-order to BST, and recursion-free post-order traversal.
    Time complexity is O(n). Space complexity is O(n).
    :param seq: seq[num]
    :return: generator[num]
    """
    it = iter(seq)
    x = next(it, None)
    if x is None:
        yield from ()
        return
    root = Node(None, x, None)
    s = [root]
    lb = -inf  # lower bound
    for x in it:
        # assert not any(y.val == lb for y in s)
        assert x > lb  # invalid input fails here
        new = Node(None, x, None)
        if x < s[-1].val:
            s[-1].left = new
        else:  # x > s[-1].val
            while len(s) > 0 and x > s[-1].val:
                last = s.pop()
            last.right = new
            lb = last.val
        s.append(new)
    yield from rec_free_post_order(root)

def convert2(seq):  # O(n^2) time solution
    it = iter(seq)
    x = next(it, None)
    if x is None:  # empty iterator
        yield from ()
        return
    path = [Node(None, x, None)]  # path from root to cursor
    for x in it:  # start iteration from seq[1]
        c = path[-1]
        if x < c.val:  # x is either the left child of cursor, or is an invalid input
            for y in path[:-1]:  # insert x from the root. it should arrive at cursor
                assert x > y.val or y.left is not None
            c.left = Node(None, x, None)
            path.append(c.left)
        else:  # x is either the right child of cursor, or a right child of an ancestor of cursor
            i = next(j for j, y in enumerate(path) if x > y.val and y.right is None)  # highest insertion point
            while len(path) > i + 1:
                yield path.pop().val
            c = path[-1]  # equivalent to path[i]
            c.right = Node(None, x, None)
            path.append(c.right)
    while len(path) > 0:  # pop everything
        yield path.pop().val

if __name__ == '__main__':
    from lib import fails_as
    from trees.construction import random_bst
    from trees.traversal import pre_order, post_order
    std_test = {(40, 30, 35, 80, 100): (35, 30, 100, 80, 40),
                (40, 30, 32, 35, 80, 90, 100, 120): (35, 32, 30, 120, 100, 90, 80, 40),
                (40, 30, 10, 35, 37, 80, 70, 60, 75, 100, 90): (10, 37, 35, 30, 60, 75, 70, 90, 100, 80, 40)}
    for k, v in std_test.items():
        assert tuple(convert(k)) == v
    fail_test = {(7, 9, 6, 1, 4, 2, 3, 40), (40, 30, 35, 20, 80, 100)}
    for x in fail_test:
        assert fails_as(AssertionError, lambda y: tuple(convert(y)), x)
    for size in range(1, 100):
        rnd_test = random_bst(size)
        assert list(convert(pre_order(rnd_test))) == list(post_order(rnd_test))
