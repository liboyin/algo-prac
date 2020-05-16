import random
import re
from itertools import tee, zip_longest
from math import floor, log2
from typing import (Any, Callable, Dict, Generator, Iterable, Iterator, List,
                    Optional, Sequence, Tuple, TypeVar, Union)

K = TypeVar('K')
T = TypeVar('T')
V = TypeVar('V')


# trivial functions
def identity(x: T) -> T:
    """The identity function."""
    return x


def fst(xs: Sequence[T]) -> T:
    """Returns the first item in a sequence."""
    assert xs
    return xs[0]


def snd(xs: Sequence[T]) -> T:
    """Returns the second item in a sequence."""
    assert len(xs) > 1, len(xs)
    return xs[1]


def compare(a: T, b: T) -> int:
    """Compares two items."""
    if a < b:
        return -1
    elif a == b:
        return 0
    return 1


# min & max
def argmin(
    iterable: Iterable[T],
    key: Callable[[T], K] = identity,
    val: bool = False,
) -> Union[int, Tuple[int, T]]:
    """Find the first index `i` where `key(iterable[i])` is the minimum.

    The entire `iterable` is consumed.

    Args:
        iterable (Iterable[T]): items to iterate
        key (Callable[[T], K]): function to extract key from each item
        val (bool): if `False`, returns the index only;
            if `True`, returns both the index and the min value

    Examples:
        >>> argmin([])
        Traceback (most recent call last):
            ...
        ValueError: min() arg is an empty sequence
        >>> argmin([2, 3, 1])
        2
        >>> argmin([2, 3, 1], val=True)
        (2, 1)
        >>> argmin('bca', key=lambda x: -ord(x))
        1
        >>> argmin('bca', key=lambda x: -ord(x), val=True)
        (1, 'c')
        >>> xs = iter('bca'); argmin(xs); next(xs)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    i, v = min(enumerate(iterable), key=lambda x: key(x[1]))
    if val:
        return i, v
    return i


def argmax(
    iterable: Iterable[T],
    key: Callable[[T], K] = identity,
    val: bool = False,
) -> Union[int, Tuple[int, T]]:
    """Find the first index `i` where `key(iterable[i])` is the maximum.

    The entire `iterable` is consumed.

    Args:
        iterable (Iterable[T]): items to iterate
        key (Callable[[T], K]): function to extract key from each item
        val (bool): if `False`, returns the index only;
            if `True`, returns both the index and the max value

    Examples:
        >>> argmax([])
        Traceback (most recent call last):
            ...
        ValueError: max() arg is an empty sequence
        >>> argmax([2, 3, 1])
        1
        >>> argmax([2, 3, 1], val=True)
        (1, 3)
        >>> argmax('bca', key=lambda x: -ord(x))
        2
        >>> argmax('bca', key=lambda x: -ord(x), val=True)
        (2, 'a')
        >>> xs = iter('bca'); argmax(xs); next(xs)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    i, v = max(enumerate(iterable), key=lambda x: key(x[1]))
    if val:
        return i, v
    return i


def argmax_2d(
    iterable: Iterable[Iterable[T]],
    key: Callable[[T], K] = identity,
    val: bool = False,
) -> Union[Tuple[int, int], Tuple[int, int, T]]:
    """Find the first index `(i, j)` where `key(iterable[i][j])` is the maximum.

    The entire `iterable` is consumed.

    Args:
        iterable (Iterable[Iterable[T]]): items to iterate
        key (Callable[[T], K]): function to extract key from each item
        val (bool): if `False`, returns the index only;
            if `True`, returns both the index and the max value

    Examples:
        >>> argmax_2d([])
        Traceback (most recent call last):
            ...
        ValueError: max() arg is an empty sequence
        >>> argmax_2d([[]])
        Traceback (most recent call last):
            ...
        ValueError: max() arg is an empty sequence
        >>> argmax_2d([[2, 3, 1], [], [5, 4]])
        (2, 0)
        >>> argmax_2d([[2, 3, 1], [], [5, 4]], val=True)
        (2, 0, 5)
        >>> argmax_2d([[2, 3, 1], [], [5, 4]], key=lambda x: -x)
        (0, 2)
        >>> argmax_2d([[2, 3, 1], [], [5, 4]], key=lambda x: -x, val=True)
        (0, 2, 1)
        >>> xs = iter([[2, 3, 1]]); argmax_2d(xs); next(xs)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    items = ((i, j, x) for i, xs in enumerate(iterable) for j, x in enumerate(xs))
    i, j, v = max(items, key=lambda x: key(x[2]))
    if val:
        return i, j, v
    return i, j


# reversing
def rev_range(fst: int, snd: Optional[int] = None) -> Iterator[int]:
    """Reversed variant of built-in `range()`, without parameter `step`.

    Examples:
        >>> list(rev_range(3))
        [2, 1, 0]
        >>> list(rev_range(1, 3))
        [2, 1]
        >>> list(rev_range(-1))
        []
    """
    if snd is None:
        return reversed(range(fst))
    return reversed(range(fst, snd))


def rev_enumerate(seq: Sequence[T]) -> Iterator[Tuple[int, T]]:
    """Reversed variant of built-in `enumerate()`, without parameter `start`.

    Note that the first parameter of `enumerate()` has type `Iterable`,
    but the equivalent parameter here must have length.

    Examples:
        >>> list(rev_enumerate([]))
        []
        >>> list(rev_enumerate('abc'))
        [(2, 'c'), (1, 'b'), (0, 'a')]
    """
    yield from zip(reversed(range(len(seq))), reversed(seq))


# indexing
def nd_getitem(*args) -> Callable[[Any], T]:
    """Call `__getitem__()` on nested objects.

    Similar to N-dimensional indexing in NumPy.

    Examples:
        >>> nd_getitem(1, 1)([[2, 3, 1], [5, 4]])
        4
        >>> nd_getitem('a', 1, 0)({'a': ['bcd', 'efg']})
        'e'
    """
    def index(x):
        for k in args:
            x = x[k]
        return x
    return index


def safe_index(
    seq: Sequence[T],
    i: int,
    default: T,
    allow_neg: bool = False,
) -> T:
    """Returns `seq[i]`. In case of an `IndexError`, returns a default value.

    Whether negative index is allowed is controlled by `allow_neg`.

    Examples:
        >>> safe_index([1, 2, 3], 1, 0)
        2
        >>> safe_index([1, 2, 3], 3, 0)
        0
        >>> safe_index([1, 2, 3], -1, 0)
        0
        >>> safe_index([1, 2, 3], -1, 0, allow_neg=True)
        3
        >>> safe_index([1, 2, 3], -4, 0, allow_neg=True)
        0

    Args:
        seq (Sequence[T]): queried sequence
        i (int): queried index
        default (T): default value
        allow_neg (bool): if `False`, returns `default` if `i` is negative,
            instead of using Python's built-in indexing
    """
    if not allow_neg and i < 0:
        return default
    try:
        return seq[i]
    except IndexError:
        return default


def kth_of_iter(
    iterable: Iterable[T],
    k: int = 0,
    default: Optional[T] = None,
) -> Optional[T]:
    """Consumes the first `k` items of the iterable, then returns the next one.

    Conceptually equivalent to `iterable[k]`.

    Args:
        iterable (Iterable[T]): items to iterate
        k (int): number of items to consume, or index of item to return
        default (Optional[T]): default value

    Examples:
        >>> kth_of_iter([])

        >>> kth_of_iter([2, 3, 1], 1)
        3
        >>> xs = iter([2, 3, 1]); (kth_of_iter(xs, 1), next(xs))
        (3, 1)
    """
    assert k >= 0, k
    for i, x in enumerate(iterable):
        if i == k:
            return x
    return default


# sorting
def is_sorted(
    iterable: Iterable[T],
    key: Callable[[T], K] = identity,
    reverse: bool = False,
) -> bool:
    """Returns whether an iterable is sorted.

    An empty iterable or an iterable with only one item are considered sorted.

    The entire `iterable` is consumed.

    Args:
        iterable (Iterable[T]): items to iterate
        key (Callable[[T], K]): function to extract key from each item
        reverse (bool): if `True`, returns whether `iterable` is sorted in reverse order

    Examples:
        >>> is_sorted([])
        True
        >>> is_sorted([], reverse=True)
        True
        >>> is_sorted([0])
        True
        >>> is_sorted([0], reverse=True)
        True
        >>> is_sorted([0, 1])
        True
        >>> is_sorted([1, 0])
        False
        >>> is_sorted([1, 0], reverse=True)
        True
        >>> is_sorted([0, 1, 0])
        False
        >>> is_sorted([0, 1, 0], reverse=True)
        False
        >>> xs = iter([0, 1, 0]); is_sorted(xs); next(xs)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    pairs = sliding_window(map(key, iterable), 2)
    if reverse:
        return all(x >= y for x, y in pairs)
    return all(x <= y for x, y in pairs)


def iter_equals(xs: Iterable[T], ys: Iterable[T]) -> bool:
    """Returns whether two iterable contain the same items.

    Note that:
    1. Two empty iterable are considered identical.
    2. Two iterable are considered different if they have different number of elements.

    Both iterables are consumed up until the point where they are not identical.

    Examples:
        >>> iter_equals([], [])
        True
        >>> iter_equals([0], [])
        False
        >>> iter_equals([0], {0})
        True
        >>> iter_equals([0, 1, 2], iter([0, 1, 2]))
        True
        >>> iter_equals([0, 1, 2], [0, 2, 1])
        False
        >>> xs = iter('abc'); ys = iter('acb'); (iter_equals(xs, ys), next(xs), next(ys))
        (False, 'c', 'b')
        >>> xs = iter('abc'); ys = iter('ac'); iter_equals(xs, ys); next(ys)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    sentinel = object()
    for x, y in zip_longest(xs, ys, fillvalue=sentinel):
        if x is sentinel or y is sentinel or x != y:
            return False
    return True


def rank(seq: Sequence[T], distinct: bool = True) -> Tuple[int, ...]:
    """Returns the rank of elements in a sequence.

    Args:
        seq (Sequence[T]): items to rank
        distinct (bool): if `False`, returns identical rank for identical items;
            if `True`, returns distinct ranks

    Examples:
        >>> rank([])
        ()
        >>> rank([2, 3, 1])
        (1, 2, 0)
        >>> rank([2, 2, 3, 1])
        (1, 2, 3, 0)
        >>> rank([2, 2, 3, 1], distinct=False)
        (1, 1, 3, 0)
    """
    a = sorted(enumerate(seq), key=snd)  # (idx, val), sorted by val
    if distinct:
        a = sorted(enumerate(a), key=nd_getitem(1, 0))  # (rank, (idx, val)), sorted by idx
    else:
        a = list(enumerate(a))  # (rank, (idx, val)), sorted by val
        for i, x in enumerate(a[1:], start=1):  # skip a[0]
            if x[1][1] == a[i - 1][1][1]:  # same val
                a[i] = (a[i - 1][0], x[1])  # tuple is immutable
        a = sorted(a, key=nd_getitem(1, 0))  # (rank, (idx, val)), sorted by idx
    return tuple(x[0] for x in a)


# filtering
def filter2(
    func: Callable[[T], K],
    iterable: Iterable[T],
) -> Tuple[List[T], List[T]]:
    """Variant of built-in `filter()` that returns both positive and negative results.

    Note that unlike built-in `filter()`, the first argument here cannot be `None`.

    The entire `iterable` is consumed.

    Args:
        func (Callable[[T], K]): filter function
        iterable (Iterable[T]): items to iterate

    Returns:
        Tuple[List[T], List[T]]: items that evaluated `False` and `True`, respectively

    Examples:
        >>> filter2(identity, [])
        ([], [])
        >>> filter2(identity, [True, False])
        ([False], [True])
        >>> filter2(identity, [(), (0,), [], [0], set(), {0}, dict(), {0: 0}])
        ([(), [], set(), {}], [(0,), [0], {0}, {0: 0}])
        >>> filter2(lambda x: x % 2, range(6))
        ([0, 2, 4], [1, 3, 5])
        >>> xs = iter([0, 1]); filter2(identity, xs); next(xs)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    result: Tuple[List[T], List[T]] = [], []  # negatives, positives
    for x in iterable:
        result[bool(func(x))].append(x)
    return result


def filter3(
    iterable: Iterable[T],
    pivot: K,
    key: Callable[[T], K] = identity,
) -> Tuple[List[T], List[T], List[T]]:
    """Given an iterable, returns items that are less than, equal to, and greater than the pivot.

    The entire `iterable` is consumed.

    Args:
        iterable (Iterable[T]): items to iterate
        pivot (K): pivot value
        key (Callable[[T], K]): function to extract key from each item

    Examples:
        >>> filter3([], None, identity)
        ([], [], [])
        >>> filter3(range(-2, 3), 0, identity)
        ([-2, -1], [0], [1, 2])
        >>> filter3(['a', 'ab', 'abc', 'b', 'bc', 'bcd'], 2, len)
        (['a', 'b'], ['ab', 'bc'], ['abc', 'bcd'])
        >>> xs = iter([0, 1, 2]); filter3(xs, 1, identity); next(xs)
        Traceback (most recent call last):
            ...
        StopIteration
    """
    result: Tuple[List[T], List[T], List[T]] = [], [], []  # lt, eq, gt
    for x in iterable:
        result[compare(key(x), pivot) + 1].append(x)
    return result


def partition(
    seq: List[T],
    pivot: K,
    key: Callable[[T], K] = identity,
) -> Tuple[List[T], int, int]:
    """In-place version of `filter3()`.

    Note that the partition result is not stable.

    Args:
        seq (List[T]): items to partition
        pivot (K): pivot value
        key (Callable[[T], K]): function to extract key from each item

    Examples:
        >>> partition([], None, identity)
        ([], 0, 0)
        >>> partition(list(range(-2, 3)), 0, identity)
        ([-2, -1, 0, 2, 1], 2, 3)
        >>> partition(['a', 'ab', 'abc', 'b', 'bc', 'bcd'], 2, len)
        (['a', 'b', 'bc', 'ab', 'bcd', 'abc'], 2, 4)
    """
    # key(seq[:i]) < pivot; key(seq[i: j]) == pivot; key(seq[k:]) > pivot
    i, j, k = 0, 0, len(seq)
    while j < k:  # consider each item in seq[j: k]
        x = key(seq[j])
        if x < pivot:
            seq[i], seq[j] = seq[j], seq[i]  # swap x with the leftmost inspected item that equals to pivot
            i += 1
            j += 1
        elif x == pivot:
            j += 1
        else:
            seq[j], seq[k - 1] = seq[k - 1], seq[j]  # swap x with the rightmost uninspected item
            k -= 1
    return seq, i, j


def filter_index(
    func: Callable[[T], K],
    iterable: Iterable[T],
) -> Generator[int, None, None]:
    """Variant of built-in `filter()` that yield indices instead of items.

    Args:
        func (Callable[[T], K]): function to extract key from each item
        iterable (Iterable[T]): items to iterate

    Examples:
        >>> list(filter_index(identity, []))
        []
        >>> list(filter_index(lambda x: x % 2, [3, 1, 4, 1, 6]))
        [0, 1, 3]
    """
    for i, x in enumerate(iterable):
        if func(x):
            yield i


# functional utils
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
            and an item from the iterable, and generates the next state
        iterable (Iterable[V]): items to iterate
        state (T): initial state
        prefix (bool): if `True`, yields the initial state immediately
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
    """Creates a sliding window with specified size on an iterable.

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
    """Repeatedly applies a transition function, yields the result, until a terminating condition is met.

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
        prefix (bool): if `True`, yields the initial state immediately,
            unless it meets the terminating condition
    """
    while term_func(state):
        if prefix:
            yield state
        prefix = True
        state = trans_func(state)


# binary search
def bin_search_left(
    seq: Sequence[T],
    x: T,
    left: int = 0,
    right: Optional[int] = None,
    key: Callable[[T], K] = identity,
) -> int:
    """Generalised re-implementation of `bisect.bisect_left()`.

    Args:
        seq (Sequence[T]): sorted Sequence to insert into
        x (T): item to insert
        left (int): left boundary of search (inclusive)
        right (Optional[int]): right boundary of search (exclusive)
        key (Callable[[T], K]): function to extract key from each item

    Returns:
        int: left-most index to insert `x` such that `seq` remains sorted after insertion
    """
    right = len(seq) - 1 if right is None else right - 1  # right is inclusive after this line
    while left <= right:
        mid = (left + right) // 2
        # side note: left + right may overflow in some other languages. use left + (right - left) // 2 instead
        if x <= key(seq[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left


def bin_search_left2(
    seq: Sequence[T],
    x: T,
    left: int = 0,
    right: Optional[int] = None,
    key: Callable[[T], K] = identity,
) -> int:
    """This algorithm appeared in Jon Bentley's Programming Pearls, sec 9.3. In this implementation,
    because step size generation is delegated to `yield_while()`, the empirical speed is about half
    that of `bin_search_left()`.

    Args:
        seq (Sequence[T]): sorted Sequence to insert into
        x (T): item to insert
        left (int): left boundary of search (inclusive)
        right (Optional[int]): right boundary of search (exclusive)
        key (Callable[[T], K]): function to extract key from each item

    Returns:
        int: left-most index to insert `x` such that `seq` remains sorted after insertion
    """
    left -= 1  # left: off the left of the search range
    if right is None:
        right = len(seq)  # right: off the right of the search range
    for step in yield_while(2 ** floor(log2(right - left)), lambda x: x > 0, lambda x: x >> 1):
        # [2 ^ floor(log_2(n)), ..., 4, 2, 1]. may include n, but not 0
        if left + step < right and key(seq[left + step]) < x:
            left += step
    return left + 1


def bin_search_right(
    seq: Sequence[T],
    x: T,
    left: int = 0,
    right: Optional[int] = None,
    key: Callable[[T], K] = identity,
) -> int:
    """Generalised re-implementation of `bisect.bisect_right()`.

    Args:
        seq (Sequence[T]): sorted Sequence to insert into
        x (T): item to insert
        left (int): left boundary of search (inclusive)
        right (Optional[int]): right boundary of search (exclusive)
        key (Callable[[T], K]): function to extract key from each item

    Returns:
        int: right-most index to insert `x` such that `seq` remains sorted after insertion
    """
    right = len(seq) - 1 if right is None else right - 1  # right is inclusive after this line
    while left <= right:
        mid = (left + right) // 2
        if x < key(seq[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return left


# misc.
def fails_as(exception, func, *args, **kwargs) -> bool:
    """Returns whether a function raises a specified exception.

    >>> fails_as(AssertionError, lambda: (_ for _ in ()).throw(AssertionError))
    True
    >>> fails_as(AssertionError, lambda: (_ for _ in ()).throw(ValueError))
    False
    """
    try:
        func(*args, **kwargs)
    except Exception as ex:
        return isinstance(ex, exception)
    else:  # if no exception is thrown
        return False


def batch_replace(text: str, rep: Dict[str, str]) -> str:
    """Batch version of `re.sub()`.

    Args:
        text (str): input text
        rep (Dict[str, str]): dictionary of replacement

    Examples:
        >>> batch_replace('', {})
        Traceback (most recent call last):
            ...
        AssertionError: empty dictionary of replacement
        >>> batch_replace('', {'a': 'b'})
        ''
        >>> batch_replace('the quick brown fox', {'the': 'a', 'fox': 'dog'})
        'a quick brown dog'
    """
    assert rep, 'empty dictionary of replacement'
    rx = re.compile('|'.join(map(re.escape, rep.keys())))
    return rx.sub(lambda x: rep[x.group(0)], text)


def randints(lower: int, upper: int, n: int) -> Tuple[int, ...]:
    """Returns a sorted tuple of `n` unique random integers within a given range.

    Args:
        lower (int): lower bound, inclusive
        upper (int): upper bound, exclusive
        n (int): number of random integers to generate
    """
    m = upper - lower + 1
    assert 0 <= n <= m, (n, m)
    rs = []
    for x in range(lower, upper + 1):
        if n == 0:
            break
        assert m >= 1  # if the loop finished by itself, m == 0 afterwards
        if random.random() <= n / m:  # not equivalent to random.randint(0, m - 1) <= n. given input (0, 1, 1),
            # the latter always outputs [0]; and with input (0, 10, 2), the latter outputs 3 elements. also note that
            # the latter is much slower as it delegates the task to random.randrange()
            rs.append(x)  # p(lower) = n / m. if lower is selected, then p(lower+1) = (n-1) / (m-1); otherwise m / (m-1)
            n -= 1
        m -= 1
    return tuple(rs)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
