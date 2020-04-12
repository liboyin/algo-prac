"""k-way Merge Algorithm using heap and iterator.

https://en.wikipedia.org/wiki/K-way_merge_algorithm
"""
from typing import Generator, Iterable, TypeVar

import heapq

T = TypeVar('T')


def merge(*iterables: Iterable[T]) -> Generator[T]:
    h = []
    for i, xs in enumerate(iterables):
        ite = iter(xs)
        for x in ite:
            # `heapq` resolves ties between tuples by looking at the next element. Here, index is
            # added as a tie breaker. This makes the output sequence is stable. Note that only the
            # first element is added.
            h.append((x, i, ite))
            break
    heapq.heapify(h)
    while h:
        x, i, ite = h[0]
        yield x
        for x in ite:  # Add the next element back to `h`, unless `ite` is exhausted
            heapq.heapreplace(h, (x, i, ite))  # more efficient than heappop + heappush
            break
        else:  # only executed when ite is exhausted
            heapq.heappop(h)


if __name__ == '__main__':
    from lib import is_sorted
    from random import randint
    for _ in range(100):
        a = [[] for _ in range(10)]
        for x in a:
            for _ in range(randint(0, 5)):
                x.append(randint(0, 10))
            x.sort()
        assert is_sorted(tuple(merge(*a)))
