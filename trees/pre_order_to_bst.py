from trees.construction import Node

def rebuild(seq):
    """
    Reconstructs a binary search tree from its pre-order traversal sequence. Note that a pre-order or post-order traversal
        sequence is sufficient to determine the structure of a BST, but an in-order traversal sequence is only sufficient
        to determine the structure subject to tree rotations. Such property does not hold for general binary tree.
    Assumes the input is a valid pre-order traversal sequence, and elements in the BST to be unique.
    :param seq: seq[T], where T is comparable
    :return: Node
    """
    it = iter(seq)
    x = next(it, None)
    assert x is not None  # empty iterator
    root = Node(None, x, None)
    s = [root]
    for x in it:  # iterate through seq[1:]
        new = Node(None, x, None)
        if x < s[-1].val:
            s[-1].left = new
        else:  # x > s[-1].val
            while len(s) > 0 and x > s[-1].val:
                last = s.pop()
            last.right = new  # select the highest insertion point
        s.append(new)
    return root

if __name__ == '__main__':
    from trees.construction import random_bst
    from trees.traversal import fast_pre_order, in_order, fast_post_order
    def iter_equals(xs, ys):
        return all(x == y for x, y in zip(xs, ys))
    for size in range(1, 100):
        rnd_test = random_bst(size)
        root = rebuild(fast_pre_order(rnd_test))
        assert iter_equals(in_order(root), in_order(rnd_test))
        assert iter_equals(fast_post_order(root), fast_post_order(rnd_test))
