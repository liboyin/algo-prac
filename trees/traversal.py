def pre_order(x):
    yield x.val
    if x.left is not None:
        yield from pre_order(x.left)  # recursive call
    if x.right is not None:
        yield from pre_order(x.right)  # recursive call

def in_order(x):
    if x.left is not None:
        yield from in_order(x.left)  # recursive call
    yield x.val
    if x.right is not None:
        yield from in_order(x.right)  # recursive call

def post_order(x):
    if x.left is not None:
        yield from post_order(x.left)  # recursive call
    if x.right is not None:
        yield from post_order(x.right)  # recursive call
    yield x.val

def rec_free_pre_order(root):
    s = [root]
    while len(s) > 0:
        x = s.pop()
        yield x.val
        if x.right is not None:
            s.append(x.right)
        if x.left is not None:
            s.append(x.left)

def rec_free_post_order(root):
    """
    Single stack, recursion-free, post-order traversal.
    Time complexity is O(n). Space complexity is O(n).
    :param root: Node[T], where T is the type of Node.val
    :return: generator[T]
    """
    d = None  # optional[Node]. indicates which direction, wrt focus, the search comes from
    s = [root]  # list[Node]. path from root to focus as a stack
    while len(s) > 0:
        c = s[-1]
        if d is None:  # cursor has not been visited
            if c.left is None:
                if c.right is None:
                    d = s.pop()  # must not replace with yield s.pop().val, as d is used in the next iteration
                    yield d.val
                else:
                    s.append(c.right)  # d is already None
            else:
                s.append(c.left)
        elif d is c.left:  # cursor is being visited the second time after its left child
            if c.right is None:
                d = s.pop()
                yield d.val
            else:
                d = None  # indicate in the next iteration, that c.right has never been visited
                s.append(c.right)
        else:  # d is s[-1].right. cursor is being visited the third time after both its children
            d = s.pop()
            yield d.val

if __name__ == '__main__':
    from lib import is_sorted
    from trees.construction import random_bst
    def iter_equals(xs, ys):
        return all(x == y for x, y in zip(xs, ys))
    for size in range(1, 100):
        rt = random_bst(size)
        assert iter_equals(pre_order(rt), rec_free_pre_order(rt))
        assert is_sorted(in_order(rt))
        assert iter_equals(post_order(rt), rec_free_post_order(rt))
