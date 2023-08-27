"""k-way Merge Algorithm using heap and iterator.

https://en.wikipedia.org/wiki/K-way_merge_algorithm
"""
import heapq
from typing import Generator, Iterable, Iterator, List, Tuple

from comparable import T

def merge(*iterables: Iterable[T]) -> Generator[T, None, None]:
    h: List[Tuple[T, int, Iterator[T]]] = []
    for i, xs in enumerate(iterables):
        iterator = iter(xs)
        # `heapq` resolves ties between tuples by looking at the next element. Here, index is
        # added as a tie breaker. This makes the output sequence stable within each input iterable.
        try:
            h.append((next(iterator), i, iterator))
        except StopIteration:
            pass
    heapq.heapify(h)
    while h:
        x, i, iterator = h[0]
        yield x
        try:  # Add the next element back to the heap
            heapq.heapreplace(h, (next(iterator), i, iterator))  # more efficient than heappop + heappush
        except StopIteration:
            heapq.heappop(h)


def test_merge():
    from lib import is_sorted
    from numpy.random import randint
    for _ in range(1000):
        assert is_sorted(merge(*(
            sorted(randint(0, 10, randint(0, 5)))
            for _ in range(10)
        )))
