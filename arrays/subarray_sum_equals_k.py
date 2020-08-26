from collections import defaultdict
from typing import DefaultDict as DefaultDictType
from typing import Sequence


def search(seq: Sequence[int], target: int) -> int:
    """560. https://leetcode.com/problems/subarray-sum-equals-k/

    Given an array of integers and a target, find the total number of continuous subarrays
    whose sum equals to the target.
    """
    csum: int = 0  # cumulative sum
    # csum -> number of continuous subarrays
    seen: DefaultDictType[int, int] = defaultdict(int)
    # not selecting anything
    seen[0] = 1
    result: int = 0
    for x in seq:  # inclusive end
        csum += x
        seen[csum] += 1
        result += seen.get(csum - target, 0)
    return result


def ref_search(seq: Sequence[int], target: int) -> int:
    N: int = len(seq)
    c: int = 0
    for i in range(N):
        for j in range(i + 1, N + 1):
            if sum(seq[i: j]) == target:
                c += 1
    return c


def test_search():
    from numpy.random import randint
    for size in range(50):
        seq = randint(0, size // 2 + 1, size)
        target = size ** 2 // 6
        print(search(seq, target), ref_search(seq, target))
