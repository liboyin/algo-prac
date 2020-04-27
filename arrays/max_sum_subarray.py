"""Kadane's algorithm of finding the subarray with the maximum sum

https://en.wikipedia.org/wiki/Maximum_subarray_problem

Observations:
    1. A max-sum subarray must start & finish with a positive number.
    2. It is safe to discard a subarray with a non-positive sum.

Time complexity is O(n). Space complexity is O(1).

Problem from Jon Bentley's Programming Pearls:
    If all elements are real numbers uniformly distributed in range [-1, 1],
    what is the expectation of this maximum sum as a function of size?

Empirical evidence seems to suggest a log-log linear relationship:
    size=31, Ex=3.299060207545906
    size=100, Ex=7.011417260111707
    size=316, Ex=12.101707427755215
    size=1000, Ex=22.20458485964562
    size=3162, Ex=40.07622280167929
    size=10000, Ex=72.16213987203754
"""
from typing import List, Tuple

from lib import argmax, stated_map


def search(arr: List[int]) -> int:
    max_sum = max(stated_map(lambda x, s: x + s if x + s > 0 else 0, arr, 0))
    if max_sum > 0:
        return max_sum
    return max(arr)  # if all elements are non-positive


def search2(arr: List[int]) -> Tuple[int, int, int]:
    """Kadane's algorithm with reconstruction."""
    start, acc = 0, 0  # start: pointer to the starting index
    max_range = 0, 0, 0  # range_start, range_end (inclusive), range_acc
    for i, x in enumerate(arr):
        if x + acc <= 0:
            acc = 0
            start = -1
        else:
            acc += x
            if start == -1:
                start = i
            if acc > max_range[2]:
                max_range = start, i, acc
    if max_range[2] > 0:
        return max_range
    i, x = argmax(arr, val=True)
    return i, i, x


if __name__ == '__main__':
    from random import randint
    def control(arr):  # O(n^3)
        n = len(arr)
        i, x = argmax(arr, val=True)
        max_range = i, i, x
        for i in range(n):
            for j in range(i, n):
                s = sum(arr[i:j+1])
                if s > max_range[2]:
                    max_range = i, j, s
        return max_range
    assert search2([-2, -3, 4, -1, -2, 1, 5, -3]) == (2, 6, 7)
    for size in range(1, 100):
        a = [randint(-size, size) for _ in range(size)]
        assert search(a) == search2(a)[2] == control(a)[2]
