from itertools import chain
from lib import bin_search_left, bin_search_right, fst, snd, stated_map, sliding_window
from math import inf
from operator import add

def search(arr):
    """
    Yields the starting and ending indices of all subarrays whose sum is zero.
    :param arr: list[int]
    :return: generator[tuple[int,int]]
    """
    n = len(arr)
    if n == 0:
        return
    appeared = {0: {0}}  # dict[int, set[int]]. sum(seq[:i]) -> i
    sum_up_to = arr[0]
    for i, x in enumerate(arr[1:], start=1):
        if sum_up_to in appeared:
            for y in appeared[sum_up_to]:
                yield y, i  # sum(arr[y, i]) == 0
            appeared[sum_up_to].add(i)
        else:
            appeared[sum_up_to] = {i}
        sum_up_to += x
    if sum_up_to in appeared:
        for y in appeared[sum_up_to]:
            yield y, n

def search2(arr):  # finds the subarray whose sum is closest to 0
    n = len(arr)
    assert n > 0
    a = list(enumerate(stated_map(add, chain([0], arr), 0)))  # (i, sum(arr[:i]))
    a.sort(key=snd)
    x, y = min(sliding_window(a, 2), key=lambda z: abs(z[0][1] - z[1][1]))
    left, right = sorted((x[0], y[0]))
    return left, right, sum(arr[left:right])

def search_k(arr, k):  # finds the subarray whose sum is closest to k
    n = len(arr)
    assert n > 0
    a = list(enumerate(stated_map(add, chain((0,), arr), 0)))  # (i, sum(arr[:i]))
    a.sort(key=snd)
    left, right = None, None
    d_min = inf
    for i, x in enumerate(a):
        js = set()
        for y in (x[1] - k, x[1] + k):  # both +k & -k are attempted as k may be positive or negative
            j = bin_search_left(a, y, key=snd)
            js.update((j - 1, j))  # on the left, on the insertion point
            js.add(bin_search_right(a, y, key=snd))  # in (extremely rare) case of duplicated values, on the right
            # example: arr = [23, 1, 9, -3, 23, 11, 11, -4, -6, 10, 0, 18], k = -11. d_min should be 1
        for y in [a[j] for j in js if 0 <= j <= n and i != j]:
            p, q = sorted((x, y), key=fst)
            diff = abs(q[1] - p[1] - k)
            if diff < d_min:
                left, right, d_min = p[0], q[0], diff
    return left, right, sum(arr[left:right]), d_min

if __name__ == '__main__':
    from random import randint
    def control(arr):
        n = len(arr)
        for i in range(n):
            for j in range(i, n):
                if sum(arr[i: j+1]) == 0:
                    yield i, j + 1
    def control_k(arr, k):
        n = len(arr)
        d_min = inf
        for i in range(n):
            for j in range(i, n):
                diff = abs(sum(arr[i:j+1]) - k)
                if diff < d_min:
                    d_min = diff
        return d_min
    for a in {(0,), (4, 6, 3, -9, -5, 1, 3, 0, 2), (4, 2, -3, 1, 6)}:
        assert set(search(a)) == set(control(a))
    for size in range(1, 100):
        for _ in range(size):
            a = [randint(-size, 2 * size) for _ in range(size)]  # 1/3 instances do not have zero-sum subarray
            c = set(control(a))
            if len(c) == 0:
                assert next(search(a), None) is None
                assert abs(search2(a)[2]) == control_k(a, 0)
            else:
                assert set(search(a)) == c
                assert search2(a)[2] == 0
            k = randint(-size, size)
            assert search_k(a, k)[-1] == control_k(a, k), (a, k, search_k(a, k), control_k(a, k))
