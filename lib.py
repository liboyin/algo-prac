import random
import re
from itertools import product, tee, zip_longest
from math import floor, log2

def identity(x):
    return x

def argmax(iterable, key=identity, val=False):  # in accordance with max(), if multiple max exist, returns the first
    r = max(enumerate(iterable), key=lambda x: key(x[1]))
    return r if val else r[0]

def argmin(iterable, key=identity, val=False):
    r = min(enumerate(iterable), key=lambda x: key(x[1]))
    return r if val else r[0]

def argmax_2d(mat, val=False):
    m, n = len(mat), len(mat[0])
    i, j = max(product(range(m), range(n)), key=lambda x: mat[x[0]][x[1]])  # lambda cannot unpack tuple in Python 3
    return (i, j, mat[i][j]) if val else (i, j)

def batch_replace(text, rep):  # rep: dict[str, str]. from_test -> to_text
    rx = re.compile('|'.join(map(re.escape, rep.keys())))
    return rx.sub(lambda x: rep[x.group(0)], text)  # re.sub accepts function as pattern

def bin_search_left(arr, x, left=0, right=None, key=identity):  # identical to bisect_left
    right = len(arr) - 1 if right is None else right - 1
    while left <= right:
        mid = (left + right) // 2
        # side note: left + right may overflow in other languages. in such case, use left + (right - left) // 2 instead
        if x <= key(arr[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left

def bin_search_left2(arr, x, left=0, right=None, key=identity):
    # this algorithm appeared in Jon Bentley's Programming Pearls sec 9.3. in this implementation, since step size
    # generation is delegated to yield_while, the empirical speed is about half of bin_search_left
    left -= 1  # left: off the left of the search range
    if right is None:
        right = len(arr)  # right: off the right of the search range
    for step in yield_while(2 ** floor(log2(right-left)), lambda x: x > 0, lambda x: x >> 1):
        # [2 ^ floor(log_2(n)), ..., 4, 2, 1]. may include n, but not 0
        if left + step < right and key(arr[left + step]) < x:
            left += step
    return left + 1

def bin_search_right(arr, x, left=0, right=None, key=identity):  # identical to bisect_right
    right = len(arr) - 1 if right is None else right - 1
    while left <= right:
        mid = (left + right) // 2
        if x < key(arr[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left

def fails_as(exception, func, *args, **kwargs):  # returns whether a function throws a specified exception
    try:
        func(*args, **kwargs)
    except Exception as ex:
        return isinstance(ex, exception)
    else:  # if no exception is thrown
        return False

def filter2(func, iterable):
    ts, fs = [], []
    for x in iterable:
        if func(x):
            ts.append(x)
        else:
            fs.append(x)
    return ts, fs

def filter3(iterable, pivot, key=identity):
    lt, eq, gt = [], [], []
    for x in iterable:
        if key(x) < pivot:
            lt.append(x)
        elif key(x) > pivot:
            gt.append(x)
        else:
            eq.append(x)
    return lt, eq, gt

def filter3_inplace(arr, pivot, key=identity):
    i, j, k = 0, 0, len(arr)  # key(arr[:i]) < pivot; key(arr[i:j]) == pivot; key(arr[k:]) > pivot
    while j < k:
        x = key(arr[j])
        if x < pivot:
            arr[i], arr[j] = arr[j], arr[i]  # swap x with the leftmost y == pivot
            i += 1
            j += 1
        elif x == pivot:
            j += 1
        else:
            arr[j], arr[k-1] = arr[k-1], arr[j]  # swap x with the rightmost unprocessed
            k -= 1
    # assert j == k
    return i, j  # note that the array rearrangement is not stable

def filter_index(func, iterable, start=0):
    for i, x in enumerate(iterable):
        if func(x):
            yield i + start

def fst(x):
    return x[0]

def is_pairwise_distinct(arr, key=identity):
    return all(key(x) != key(y) for x, y in sliding_window(arr, 2))

def is_sorted(arr, key=identity):
    return all(key(x) <= key(y) for x, y in sliding_window(arr, 2))

def iter_equals(xs, ys):
    sentinel = object()
    return all((x is not sentinel and y is not sentinel and x == y) for x, y in zip_longest(xs, ys, fillvalue=sentinel))

def kth_of_iter(iterable, k=0, default=None):
    """
    Returns the kth item in an iterable, or the last element if k == 0. If k > len(iterable), returns the default value.
    :param iterable: iterable[T]
    :param k: int. cardinal number unless k == 0
    :param default: Any
    :return: Union(T, type(default))
    """
    assert k >= 0
    k -= 1  # to ordinal number
    i, x = -1, default
    for i, x in enumerate(iterable):
        if i == k:
            return x
    return x  # covers k == -1 or k > len(iterable) or empty iterator

def np_index(*idx):  # NumPy style indexing
    def index(x):
        for i in idx:
            x = x[i]
        return x
    return index

def randints(lower, upper, n):  # returns a sorted list of n unique random integers within a given range
    m = upper - lower + 1
    assert 0 <= n <= m
    r = []
    for x in range(lower, upper+1):
        if n == 0:
            break
        assert m >= 1  # if the loop finished by itself, m == 0 afterwards
        if random.random() <= n / m:  # not equivalent to random.randint(0, m - 1) <= n. given input (0, 1, 1),
            # the latter always outputs [0]; and with input (0, 10, 2), the latter outputs 3 elements. also note that
            # the latter is much slower as it delegates the task to random.randrange()
            r.append(x)  # p(lower) = n / m. if lower is selected, then p(lower+1) = (n-1) / (m-1); otherwise m / (m-1)
            n -= 1
        m -= 1
    return r

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
    for x in [x.split('=')[0] for x in re.split(',\s*', args)]:  # \s matches any whitespace chars
        code.append('\t\tself.{0} = {0}'.format(x))
    exec('\n'.join(code), scope)
    return scope[name]

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

def snd(x):
    return x[1]

def stated_map(func, iterable, state, prefix=False):
    if prefix:
        yield state
    for x in iterable:
        state = func(x, state)
        yield state

def sliding_window(iterable, size):
    iters = tee(iterable, size)
    for i in range(size):
        for _ in range(i):
            next(iters[i], None)
    return zip(*iters)

def yield_while(state, term, trans):
    while term(state):
        yield state
        state = trans(state)
