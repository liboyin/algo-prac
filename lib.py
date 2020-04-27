import random
import re
from itertools import product, tee, zip_longest
from math import floor, log2
from typing import (Any, Callable, Dict, Generator, Iterable, Iterator, List,
                    Optional, Sequence, Tuple, TypeVar, Union)

T = TypeVar('T')
V = TypeVar('V')


def identity(x: T) -> T:
    """The identity function."""
    return x


def argmax(
    iterable: Iterable[T],
    key: Callable[[T], Any] = identity,
    val: bool = False
) -> Union[int, Tuple[int, T]]:
    """Find the first index `i` where `key(iterable[i])` is the maximum.

    Also see `argmin()`.

    Args:
        iterable (Iterable[T]): items to iterate
        key (Callable[[T], Any], optional): function of one element to extract key for each element
        val (bool, optional): if False, returns index only; if True, returns index and max value
    """
    r: Tuple[int, T] = max(enumerate(iterable), key=lambda x: key(x[1]))
    return r if val else r[0]


def argmin(iterable: Iterable[T], key: Callable = identity, val: bool = False) -> Union[int, Tuple[int, T]]:
    """Find the first index `i` where `key(iterable[i])` is the minimum.

    Also see `argmin()`.

    Args:
        iterable (Iterable[T]): items to iterate
        key (Callable[[T], Any], optional): function of one element to extract key for each element
        val (bool, optional): if False, returns index only; if True, returns index and min value
    """
    r: Tuple[int, T] = min(enumerate(iterable), key=lambda x: key(x[1]))
    return r if val else r[0]


def argmax_2d(mat: Sequence[Sequence[T]], val: bool = False) -> Union[Tuple[int, int], Tuple[int, int, T]]:
    """Find the first index pair ``(i, j)`` s.t. ``mat[i][j]`` is the maximum.

    Args:
        mat: must be indexed
        val: if False, returns index pair ``(i, j)`` only; if True, returns ``(i, j, mat[i][j])``

    Returns:
        see ``val``
    """
    # TODO: make iterator-based s.t. runs on non-regular form
    m, n = len(mat), len(mat[0])
    i, j = max(product(range(m), range(n)), key=lambda x: mat[x[0]][x[1]])
    return (i, j, mat[i][j]) if val else (i, j)


def batch_replace(text: str, rep: Dict[str, str]) -> str:
    """
    Batch version of ``re.sub()``.

    Args:
        text: input text
        rep: dictionary of replacement

    Returns:
        replaced text
    """
    rx = re.compile('|'.join(map(re.escape, rep.keys())))
    # re.sub accepts function as pattern
    return rx.sub(lambda x: rep[x.group(0)], text)


def bin_search_left(arr: Sequence[T], x: T, left: int = 0, right: Optional[int] = None,
                    key: Callable[[T], Any] = identity) -> int:
    """Generalised re-implementation of ``bisect.bisect_left()``.

    Args:
        arr: sorted list to search in
        x: item to insert
        left: left boundary of search (inclusive)
        right: right boundary of search (exclusive)
        key: mapping function s.t. search is equivalently performed on ``map(key, arr)``

    Returns:
        left-most index to insert ``x`` such that ``arr`` remains sorted after insertion
    """
    right = len(arr) - 1 if right is None else right - 1  # right is inclusive after this line
    while left <= right:
        mid = (left + right) // 2
        # side note: left + right may overflow in some other languages. use left + (right - left) // 2 instead
        if x <= key(arr[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left


def bin_search_left2(arr: Sequence[T], x: T, left: int = 0, right: Optional[int] = None,
                     key: Callable = identity) -> int:
    """This algorithm appeared in Jon Bentley's Programming Pearls, sec 9.3. In this implementation, since step size
    generation is delegated to ``yield_while``, the empirical speed is about half of ``bin_search_left()``.

    Args:
        arr: sorted list to search in
        x: item to insert
        left: left boundary of search (inclusive)
        right: right boundary of search (exclusive)
        key: mapping function s.t. search is equivalently performed on ``map(key, arr)``

    Returns:
        left-most index to insert ``x`` such that ``arr`` remains sorted after insertion
    """
    left -= 1  # left: off the left of the search range
    if right is None:
        right = len(arr)  # right: off the right of the search range
    for step in yield_while(2 ** floor(log2(right - left)), lambda x: x > 0, lambda x: x >> 1):
        # [2 ^ floor(log_2(n)), ..., 4, 2, 1]. may include n, but not 0
        if left + step < right and key(arr[left + step]) < x:
            left += step
    return left + 1


def bin_search_right(arr: Sequence[T], x: T, left: int = 0, right: Optional[int] = None,
                     key: Callable = identity) -> int:
    """Generalised re-implementation of ``bisect.bisect_right()``.

    Args:
        arr: sorted list to search in
        x: item to insert
        left: left boundary of search (inclusive)
        right: right boundary of search (exclusive)
        key: mapping function s.t. search is equivalently performed on ``map(key, arr)``

    Returns:
        right-most index to insert ``x`` such that ``arr`` remains sorted after insertion
    """
    right = len(arr) - 1 if right is None else right - 1  # right is inclusive after this line
    while left <= right:
        mid = (left + right) // 2
        if x < key(arr[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left


def fails_as(exception, func, *args, **kwargs):
    # returns whether a function throws a specified exception
    # TODO: replace with unittest.AssertRaises()
    try:
        func(*args, **kwargs)
    except Exception as ex:
        return isinstance(ex, exception)
    else:  # if no exception is thrown
        return False


def filter2(func: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[List[T], List[T]]:
    """Re-implementation of ``filter()`` that returns both positive and negative results.

    Returns:
        list of negative, list of positives
    """
    rs: Tuple[List[T], List[T]] = ([], [])  # (negatives, positives)
    for x in iterable:
        rs[int(func(x))].append(x)
    return rs


def filter3(iterable: Iterable[T], pivot: T, key=identity):
    lt, eq, gt = [], [], []
    for x in iterable:
        k = key(x)
        if k < pivot:
            lt.append(x)
        elif k > pivot:
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
            arr[j], arr[k - 1] = arr[k - 1], arr[j]  # swap x with the rightmost unprocessed
            k -= 1
    # assert j == k
    return i, j  # note that the array rearrangement is not stable


def filter_index(func, iterable, start=0):
    for i, x in enumerate(iterable):
        if func(x):
            yield i + start


def fst(xs: Sequence[T]) -> T:
    """Return the first element in a sequence."""
    assert len(xs) > 0
    return xs[0]


def is_sorted(iterable: Iterable[T], key: Callable[[T], Any] = identity) -> bool:
    """Return whether an iterable is sorted. Consumes the iterable.

    Args:
        iterable (Iterable[T]): [description]
        key (Callable[[T], Any], optional): [description]. Defaults to identity.
    """
    return all(key(x) <= key(y) for x, y in sliding_window(iterable, 2))


def iter_equals(xs: Iterable[T], ys: Iterable[T]) -> bool:
    """Return whether two iterables contain the same elements. Consumes both iterables.

    Two iterables are considered different if they have different length.

    Examples:
        >>> iter_equals(iter([1, 2, 3]), iter([1, 2, 3]))
        True
        >>> iter_equals(iter([1, 2, 3]), iter([2, 3, 1]))
        False
        >>> iter_equals(iter([1, 2, 3]), iter([1, 2]))
        False
        >>> iter_equals(iter([]), iter([]))
        True
    """
    sentinel = object()
    for x, y in zip_longest(xs, ys, fillvalue=sentinel):
        if x is sentinel or y is sentinel or x != y:
            return False
    return True


def kth_of_iter(iterable, k=0, default=None):
    assert k >= 0
    k -= 1  # to ordinal number
    i, x = -1, default
    for i, x in enumerate(iterable):
        if i == k:
            return x
    return x  # covers k == -1 or k > len(iterable) or empty iterator


def np_index(*idx: int):  # NumPy style indexing for Python objects
    def index(x):
        for i in idx:
            x = x[i]
        return x
    return index


def randints(lower, upper, n):  # returns a sorted list of n unique random integers within a given range
    m = upper - lower + 1
    assert 0 <= n <= m
    r = []
    for x in range(lower, upper + 1):
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
    a = sorted(enumerate(arr), key=snd)  # (idx, val), sorted by val
    if distinct:
        a = sorted(enumerate(a), key=np_index(1, 0))  # (rank, (idx, val)), sorted by idx
    else:
        a = list(enumerate(a))  # (rank, (idx, val)), sorted by val
        for i, x in enumerate(a[1:], start=1):  # skip a[0]
            if x[1][1] == a[i - 1][1][1]:  # same val
                a[i] = a[i - 1][0], x[1]  # tuple is immutable
        a = sorted(a, key=np_index(1, 0))  # (rank, (idx, val)), sorted by idx
    return [x[0] for x in a]


def rev_range(
    fst: int,
    snd: Optional[int] = None
) -> Iterator[int]:
    """Reversed version of built-in `range()`, without the step argument.

    Examples:
        >>> list(rev_range(5))
        [4, 3, 2, 1, 0]
        >>> list(rev_range(1, 5))
        [4, 3, 2, 1]
        >>> list(rev_range(-1))
        []
    """
    return reversed(range(fst) if snd is None else range(fst, snd))


def rev_enumerate(seq: Sequence[T]) -> Iterator[Tuple[int, T]]:
    """Reversed variant of built-in `enumerate()`, without the start argument.

    Note that the first argument of `enumerate()` has type `Iterable`, but the equivalent argument here must have length.

    Examples:
        >>> list(rev_enumerate('abc'))
        [(2, 'c'), (1, 'b'), (0, 'a')]
    """
    yield from zip(reversed(range(len(seq))), reversed(seq))


def safe_query(
    seq: Sequence[T],
    i: int,
    default: T,
    allow_neg: bool = False,
) -> T:
    """Query a sequence. In case of an IndexError, return a default value.

    Whether negative index is allowed is controlled by `allow_neg`.

    Examples:
        >>> safe_query([1, 2, 3], 1, 0)
        2
        >>> safe_query([1, 2, 3], 3, 0)
        0
        >>> safe_query([1, 2, 3], -1, 0)
        0
        >>> safe_query([1, 2, 3], -1, 0, allow_neg=True)
        3

    Args:
        seq (Sequence[T]): queried sequence
        i (int): queried index
        default (T): default value
        allow_neg (bool, optional): if False, return `default` if `i` is negative
    """
    if not allow_neg and i < 0:
        return default
    try:
        return seq[i]
    except IndexError:
        return default


def snd(xs: Sequence[T]) -> T:
    """Return the second element in a sequence.

    Args:
        xs (Sequence[T]): queried sequence
    """
    assert len(xs) > 1, len(xs)
    return xs[1]


def stated_map(
    func: Callable[[T, V], T],
    iterable: Iterable[V],
    state: T,
    prefix: bool = True,
) -> Generator[T, None, None]:
    """A stated variant of `map()`.

    Whether the initial state is yielded is controlled by `prefix`.

    Also see `yield_while()`.

    Examples:
        >>> list(stated_map(lambda x, y: x * y, [2, 3, 4], 1))
        [1, 2, 6, 24]
        >>> list(stated_map(lambda x, y: x * y, [2, 3, 4], 1, prefix=False))
        [2, 6, 24]

    Args:
        func (Callable[[T, V], T]): a function that takes in the current state 
            and an element from the iterable, and generates the next state
        iterable (Iterable[V]): items to iterate
        state (T): initial state
        prefix (bool, optional): if True, yield the initial state immediately
    """
    if prefix:
        yield state
    for x in iterable:
        state = func(state, x)
        yield state


def sliding_window(
    iterable: Iterable[T],
    size: int,
) -> Iterator[Tuple[T, ...]]:
    """Create a sliding window with specified size on a given iterable object.

    Examples:
        >>> list(sliding_window(range(5), size=3))
        [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
        >>> list(sliding_window(range(5), size=0))
        []

    Args:
        iterable (Iterable[T]): items to iterate
        size (int): size of the sliding window
    """
    iterators: Tuple[Iterator[T], ...] = tee(iterable, size)
    for i in range(size):
        for _ in range(i):
            next(iterators[i], None)
    return zip(*iterators)


def yield_while(
    state: T,
    term_func: Callable[[T], bool],
    trans_func: Callable[[T], T],
    prefix: bool = True,
) -> Generator[T, None, None]:
    """Repeatedly apply a transition function, yield the result, until a terminating condition is met.

    Whether the initial state is yielded is controlled by `prefix`.

    Also see `stated_map()`.

    Examples:
        >>> list(yield_while(1, lambda x: x < 10, lambda x: x * 2))
        [1, 2, 4, 8]
        >>> list(yield_while(1, lambda x: x < 10, lambda x: x * 2, prefix=False))
        [2, 4, 8]
        >>> list(yield_while(10, lambda x: x < 10, lambda x: x * 2))
        []

    Args:
        state (T): initial state
        term_func (Callable[[T], bool]): terminating function
        trans_func (Callable[[T], T]): transition function
        prefix (bool, optional): if True, yield the initial state immediately,
            unless it meets the terminating condition
    """
    while term_func(state):
        if prefix:
            yield state
        prefix = True
        state = trans_func(state)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
