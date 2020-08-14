"""
MergeSort with iterators.
"""
from itertools import chain
from typing import Generator, Iterator, Sequence, TypeVar

from more_itertools import peekable

T = TypeVar('T')


def mergesort(xs: Sequence[T]) -> Generator[T, None, None]:
    if len(xs) <= 1:
        yield from xs
    else:
        mid = len(xs) // 2
        left = peekable(mergesort(xs[:mid]))  # recursive call
        right = peekable(mergesort(xs[mid:]))  # recursive call
        yield from merge(left, right)


def merge(xs: peekable, ys: peekable) -> Generator[T, None, None]:
    try:
        while True:
            yield next(xs) if xs.peek() <= ys.peek() else next(ys)
    except StopIteration:
        yield from chain(xs, ys)


def test_mergesort():
    import numpy as np
    for i in range(32):
        arr = np.random.randint(0, i, i)
        assert list(mergesort(arr)) == sorted(arr), (list(mergesort(arr)), sorted(arr))
