"""
MergeSort with iterators.
"""
from itertools import chain
from typing import Generator, Sequence

from comparable import T
from lib import PeekableIterator


def mergesort(xs: Sequence[T]) -> Generator[T, None, None]:
    if len(xs) <= 1:
        yield from xs
    else:
        mid = len(xs) // 2
        left = PeekableIterator(mergesort(xs[:mid]))  # recursive call
        right = PeekableIterator(mergesort(xs[mid:]))  # recursive call
        yield from merge(left, right)


def merge(xs: PeekableIterator[T], ys: PeekableIterator[T]) -> Generator[T, None, None]:
    try:
        while True:
            yield next(xs) if xs.peek() <= ys.peek() else next(ys)
    except StopIteration:
        yield from chain(xs, ys)


def test_mergesort():
    from numpy.random import randint
    for i in range(32):
        arr = randint(0, i, i)
        assert list(mergesort(arr)) == sorted(arr)
