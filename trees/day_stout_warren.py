from trees.construction import Node
from math import log2, floor

def tree_to_vine(root):
    """
    Converts a tree to a right-singly-linked list, i.e. a degenerate tree, or a vine, in place, recursion-free.
    Root must not to have a left child. This is usually achieved by creating a pseudo-root whose left child is None,
        and right child is the original root.
    After the process, left pointers contain unpredictable values.
    Time complexity is O(n). Space complexity is O(1).
    :param root: Node
    """
    assert root.left is None
    tail = root  # tail of the portion known to be the initial segment of the vine
    rest = root.right  # root of the portion which may need additional work. rest is rail.right always holds
    while rest is not None:
        assert rest is tail.right
        if rest.left is None:  # a node with no left child can be added to the tail of the vine. this happens exactly n times
            tail = rest
            rest = rest.right
        else:  # rotate right: ((ll, left, lr), rest, right) -> (ll, left, (lr, rest, right))
            temp = rest.left
            rest.left = temp.right
            temp.right = rest
            rest = temp
            tail.right = temp

def vine_to_tree(root, size):
    """
    Produces a balanced and complete tree by repeatedly left rotating every second node on the vine.
    Time complexity is O(n). Space complexity is O(1).
    :param root: Node, pseudo-root of a vine
    :param size: int, positive
    """
    def compress(n):
        x = root
        for _ in range(n):
            # left rotation on right: (left, x, (rl, right, (rrl, rr, rrr))) -> (left, x, ((rl, right, rrl), rr, rrr))
            temp = x.right
            x.right = temp.right
            x = x.right  # x ends up on rr, i.e. right child of original position
            temp.right = x.left
            x.left = temp
    assert root.left is None
    assert size > 0
    m = 2 ** floor(log2(size + 1)) - 1  # TODO: ???
    compress(size - m)
    while m > 1:
        m //= 2
        compress(m)

def day_stout_warren(root):
    """
    Re-balances a binary search tree in-place, recursion-free.
    ref: Tree Rebalancing in Optimal Time and Space, Stout et al., ACM Communications, September 1986
    Time complexity is O(n). Space complexity is O(1).
    :param root: Node
    :return: tuple[Node,int]. root and tree size
    """
    pseudo_root = Node(None, None, root)
    tree_to_vine(pseudo_root)
    x, c = pseudo_root, 0
    while x.right is not None:
        x = x.right
        c += 1
    vine_to_tree(pseudo_root, c)
    return pseudo_root.right, c

def max_height_diff(root):
    def step(x):
        if x is None:
            return 0, 0
        l_depth, l_diff = step(x.left)  # recursive call
        r_depth, r_diff = step(x.right)  # recursive call
        depth = max(l_depth, r_depth) + 1
        diff = max(l_diff, r_diff, abs(l_depth - r_depth))
        return depth, diff
    return step(root)[1]

if __name__ == '__main__':
    from lib import iter_equals
    from trees.construction import random_bst
    from trees.traversal import in_order
    for size in [x for x in range(1, 100) for _ in range(x)]:
        t = random_bst(size)
        d = max_height_diff(t)
        control = list(in_order(t))
        r, c = day_stout_warren(t)
        assert c == size
        assert iter_equals(in_order(r), control)
        assert max_height_diff(r) <= d
