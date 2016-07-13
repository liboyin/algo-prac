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

def fast_pre_order(root):
    s = [root]
    while len(s) > 0:
        x = s.pop()
        yield x.val
        if x.right is not None:
            s.append(x.right)
        if x.left is not None:
            s.append(x.left)

def fast_in_order(root):
    s = [(root, False)]
    while len(s) > 0:
        x, v = s[-1]  # v: whether the left child is visited
        if x is None:
            s.pop()
            continue
        if v:
            yield x.val
            s.pop()
            s.append((x.right, False))
        else:
            s[-1] = x, True
            s.append((x.left, False))

def fast_post_order(root):
    s = [(root, 0)]
    while len(s) > 0:
        x, v = s[-1]  # v = 0: left child unvisited; 1: left child visited, but right child not; 2: right child visited
        if x is None:
            s.pop()
            continue
        if v == 0:
            s[-1] = x, 1
            s.append((x.left, 0))
        elif v == 1:
            s[-1] = x, 2
            s.append((x.right, 0))
        else:
            yield x.val
            s.pop()

if __name__ == '__main__':
    from trees.construction import random_bst
    def iter_equals(xs, ys):
        return all(x == y for x, y in zip(xs, ys))
    for size in range(1, 100):
        rt = random_bst(size)
        assert iter_equals(pre_order(rt), fast_pre_order(rt))
        assert iter_equals(in_order(rt), fast_in_order(rt))
        assert iter_equals(post_order(rt), fast_post_order(rt))
