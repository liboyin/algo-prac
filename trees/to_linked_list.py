from trees.construction import Node
from trees.day_stout_warren import tree_to_vine

def convert(root):
    """
    Converts a binary tree to a doubly-linked list in place with recursion.
    Time complexity is O(n). Space complexity is O(n).
    :param root: Node
    :return: tuple[Node,Node,int]. head, tail, and size of the doubly-linked list
    """
    if root.left is None:
        ll, lc = root, 0
    else:
        ll, lr, lc = convert(root.left)  # left & right of the left subtree. recursive call
        lr.right = root
        root.left = lr
    if root.right is None:
        rr, rc = root, 0
    else:
        rl, rr, rc = convert(root.right)  # left & right of the right subtree. recursive call
        rl.left = root
        root.right = rl
    return ll, rr, lc + rc + 1

def rec_free_convert(root):
    pseudo_root = Node(None, None, root)
    tree_to_vine(pseudo_root)  # subprocedure of Day-Stout-Warren
    x, c = pseudo_root.right, 1
    while x.right is not None:
        x.right.left = x  # set reverse pointers
        x = x.right
        c += 1
    return pseudo_root.right, x, c

if __name__ == '__main__':
    from copy import deepcopy
    from lib import yield_while
    from trees.construction import random_bst
    for size in range(1, 100):
        rnd_test = random_bst(size)
        test_copy = deepcopy(rnd_test)
        rec_head, rec_tail, rec_size = convert(rnd_test)
        rec_fwd = list(yield_while(rec_head, lambda x: x is not None, lambda x: x.right))
        assert len(rec_fwd) == rec_size
        assert rec_fwd[-1] == rec_tail
        rec_bkwd = list(yield_while(rec_tail, lambda x: x is not None, lambda x: x.left))
        assert rec_fwd == rec_bkwd[::-1]
        rf_head, rf_tail, rf_size = rec_free_convert(test_copy)
        rf_fwd = list(yield_while(rf_head, lambda x: x is not None, lambda x: x.right))
        assert rf_fwd == rec_fwd
        rf_bkwd = list(yield_while(rf_tail, lambda x: x is not None, lambda x: x.left))
        assert rf_bkwd == rec_bkwd
