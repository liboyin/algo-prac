import re
from itertools import product, tee
from math import floor, log2

def identity(x):
    return x

def argmax(iterable, key=identity, val=False):  # if multiple global max exist, returns the first one
    r = max(enumerate(iterable), key=lambda x: key(x[1]))
    return r if val else r[0]

def argmin(iterable, key=identity, val=False):
    return argmax(iterable, key=lambda x: -key(x), val=val)

def argmax_2d(mat, val=False):
    m, n = len(mat), len(mat[0])
    i, j = max(product(range(m), range(n)), key=lambda x: mat[x[0]][x[1]])  # lambda cannot unpack tuple in Python3
    if val:
        return i, j, mat[i][j]
    return i, j

def bin_search_left(arr, x, left=0, right=None, key=identity):
    right = len(arr) - 1 if right is None else right - 1
    while left <= right:
        mid = (left + right) // 2
        if x <= key(arr[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left

def bin_search_left2(arr, x, left=0, right=None, key=identity):
    left -= 1  # left: on the left (exclusive) of the search point
    if right is None:
        right = len(arr)  # right: on the right (exclusive) of search range
    for step in yield_while(2 ** floor(log2(right-left)), lambda x: x > 0, lambda x: x >> 1):
        # [2 ^ floor(log_2(n)), ..., 4, 2, 1]. may include n, but not 0
        if left + step < right and key(arr[left + step]) < x:
            left += step
    return left + 1

def bin_search_left(arr, x, left=0, right=None, key=identity):
    right = len(arr) - 1 if right is None else right - 1
    while left <= right:
        mid = (left + right) // 2
        if x < key(arr[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left

def filter2(func, iterable):
    ts, fs = [], []
    for x in iterable:
        if func(x):
            ts.append(x)
        else:
            fs.append(x)
    return ts, fs

def filter3(pivot, iterable, func=identity):
    lt, eq, gt = [], [], []
    for x in iterable:
        if func(x) < pivot:
            lt.append(x)
        elif func(x) > pivot:
            gt.append(x)
        else:
            eq.append(x)
    return lt, eq, gt

def filter_index(func, iterable, start=0):
    for i, x in enumerate(iterable):
        if func(x):
            yield i + start

def is_pairwise_distinct(arr, key=identity):
    return all(key(x) != key(y) for x, y in sliding_window(arr, 2))

def is_sorted(arr, key=identity):
    return all(key(x) <= key(y) for x, y in sliding_window(arr, 2))

def kth_of_iter(iterable, k=0, default=None):
    """
    Returns the kth item in an iterable, or the last element if k=0. If k > len(iterable), returns the default value.
    :param iterable: iterable[T]
    :param k: int. cardinal number if k != 0
    :param default: Any
    :return: Union(T, type(default))
    """
    assert k >= 0
    k -= 1
    i, x = -1, default
    for i, x in enumerate(iterable):
        if i == k:
            return x
    return x  # k == -1 or k > len(iterable) or empty iterator

def np_index(*idx):  # NumPy style indexing
    def index(x):
        for i in idx:
            x = x[i]
        return x
    return index

def rank(arr, distinct=True):
    a = sorted(enumerate(arr), key=np_index(1))  # (idx, val), sorted by val
    if distinct:
        a = sorted(enumerate(a), key=np_index(1, 0))  # (rank, (idx, val)), sorted by idx
    else:
        a = list(enumerate(a))  # (rank, (idx, val)), sorted by val
        for i, x in enumerate(a[1:], start=1):  # skip a[0]
            if x[1][1] == a[i-1][1][1]:  # same val
                a[i] = a[i-1][0], x[1]  # tuple is immutable
        a = sorted(a, key=np_index(1, 0))  # (rank, (idx, val)), sorted by idx
    return [x[0] for x in a]

def record_class(name, args, scope):
    # by design, default arguments are instantiated only once. mutable default value will cause aliasing
    code = ['class {}:'.format(name), '\tdef __init__(self, {}):'.format(args)]
    for x in [x.split('=')[0] for x in re.split(', *', args)]:
        code.append('\t\tself.{0} = {0}'.format(x))
    exec('\n'.join(code), scope)
    return scope[name]

def remove_duplicates(iterable):
    # side note: duplication removal on array must be performed backwards:
    # for i in rev_range(len(arr) - 1):
    #     if arr[i] == arr[i+1]:
    #         del arr[i]  # O(n^2) time in total
    it = iter(iterable)
    prev = next(it)  # if iterable is empty, raises StopIteration
    yield prev
    for x in it:
        if x != prev:
            yield x
            prev = x

def replace_multi(text, rep):  # rep: dict[str, str]. from_test -> to_text
    rx = re.compile('|'.join(map(re.escape, rep.keys())))
    return rx.sub(lambda x: rep[x.group(0)], text)  # re.sub accepts function as pattern

def rev_enumerate(iterable):
    return reversed(list(enumerate(iterable)))

def rev_range(fst, snd=None):
    if snd is None:
        return reversed(range(fst))
    return reversed(range(fst, snd))

def safe_query(arr, i, default):
    if i < 0 or i >= len(arr):
        return default
    return arr[i]

def stated_map(func, iterable, state):
    for x in iterable:
        state = func(x, state)
        yield state

def sliding_window(iterable, size):
    iters = tee(iterable, size)
    for i in range(size):
        for _ in range(i):
            next(iters[i], None)
    return zip(*iters)

def yield_while(state, term, next):
    while term(state):
        yield state
        state = next(state)
