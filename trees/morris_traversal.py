from trees.construction import Node

def predecessor(x):  # predecessor is a bijective function
    c = x.left
    assert c is not None
    while c.right is not None and c.right is not x:  # ignore back pointer
        c = c.right
    return c

def in_order(root):
    """
    Morris in-order traversal: Traverses a tree in-order without recursion or stack.
    The algorithm utilises empty pointers of nodes. The tree is modified while being traversed, but all modifications
        are reverted before the algorithm finishes. Note that this algorithm is thread/iterator unsafe.
    Time complexity is O(n). Space complexity is O(1).
    :param root: Node[T]
    :return: generator[T]
    """
    x = root
    while x is not None:
        if x.left is None:
            yield x.val
            x = x.right  # may follow a back pointer
        else:
            p = predecessor(x)
            if p.right is None:  # first visit to x
                # for pre-order traversal, yield x.val here
                p.right = x  # set back pointer
                x = x.left
            else:  # second visit to x
                assert p.right is x
                p.right = None  # remove back pointer
                yield x.val
                x = x.right

def post_order(root):
    """
    Traverse a tree post-order without recursion or stack.
    The solution is based on Morris in-order retrieval. When a node x is visited the second time, nodes on the path from
        x.left to predecessor(x) (inclusive start & finish) are yielded in reversed order.
    Time complexity is O(n). Space complexity is O(1).
    :param root: Node[T]
    :return: generator[T]
    """
    x = Node(root, None, None)  # retrieval terminates on pseudoroot.right, skipping pseudoroot itself
    while x is not None:
        if x.left is None:
            x = x.right
        else:
            p = predecessor(x)
            if p.right is None:  # first visit to x
                p.right = x
                x = x.left
            else:  # second visit to x
                assert p.right is x
                # reverse right pointers of all nodes on the path from x to p. note how x.right is intact
                head = x
                mid = x.left
                while mid is not x:
                    tail = mid.right
                    mid.right = head
                    head = mid
                    mid = tail
                # reset right pointers
                head = x
                mid = p
                while mid is not x:
                    yield mid.val
                    tail = mid.right
                    mid.right = head
                    head = mid
                    mid = tail
                p.right = None
                x = x.right

if __name__ == '__main__':
    from trees.construction import random_bst
    from trees.traversal import fast_in_order, fast_post_order
    for size in range(1, 100):
        for _ in range(size):
            t = random_bst(size)
            assert list(in_order(t)) == list(fast_in_order(t))
            assert list(post_order(t)) == list(fast_post_order(t))
