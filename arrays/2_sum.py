from typing import Dict, Sequence, Tuple


def search(seq: Sequence[int], target: int) -> Tuple[int, int]:
    """1. https://leetcode.com/problems/two-sum/

    Given an array of integers, return indices of the two numbers that add up to a specific target.

    You may assume that each input would have exactly one solution and you may not use the same element twice.
    """
    seen: Dict[int, int] = {}
    for i, x in enumerate(seq):
        y = target - x
        if y in seen:
            return seen[y], i
        seen[x] = i
    return -1, -1


def search_sorted(seq: Sequence[int], target: int) -> Tuple[int, int]:
    """167. https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

    Given an array of integers sorted in ascending order, return indices of the two numbers that add up to a specific target.

    You may assume that each input would have exactly one solution and you may not use the same element twice.
    """
    N = len(seq)
    if N < 2:
        return -1, -1
    i = 0
    j = N - 1
    while i < j:
        s = seq[i] + seq[j]
        if s == target:
            return i, j
        if s < target:
            i += 1
        else:
            j -= 1
    return -1, -1


def ref_search(seq: Sequence[int], target: int) -> Tuple[int, int]:
    N = len(seq)
    if N < 2:
        return -1, -1
    for i in range(N - 1):
        for j in range(i + 1, N):
            if seq[i] + seq[j] == target:
                return i, j
    return -1, -1


def test_search():
    from collections import Counter
    from itertools import combinations
    from numpy.random import randint
    n = 3
    while n < 10:
        seq = randint(-n, n + 1, 2 * n).tolist()
        c = Counter(x + y for x, y in combinations(seq, r=2))
        sums = [k for k, v in c.items() if v == 1]
        if len(sums) == 1:
            k = sums[0]
            assert search(seq, k) == ref_search(seq, k)
            seq.sort()
            assert search_sorted(seq, k) == ref_search(seq, k)
            n += 1
