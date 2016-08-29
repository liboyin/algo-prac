from lib import bin_search_left, bin_search_right, snd, stated_map, sliding_window
from math import inf
from operator import add

def search(arr):
    """
    Finds the subarray whose sum is closest to 0. If multiple such subarrays exist, returns the first one.
    :param arr: list[num]
    :return: tuple[int,int]
    """
    assert len(arr) > 0
    a = list(enumerate(stated_map(add, arr, 0, prefix=True)))  # (i, sum(arr[:i])), i in [0, n]
    a.sort(key=snd)  # stable sort
    x, y = min(sliding_window(a, 2), key=lambda z: abs(z[0][1] - z[1][1]))
    left, right = sorted((x[0], y[0]))
    return left, right

def search_k(arr, k):
    """
    Finds the subarray whose sum is closest to k. If multiple such subarrays exist, there is no guarantee on which
        one is returned.
    Time complexity is O(n\log n). Space complexity is O(n).
    :param arr: list[num]
    :param k: num
    :return: tuple[int,int]
    """
    n = len(arr)
    assert n > 0
    a = sorted(enumerate(stated_map(add, arr, 0, prefix=True)), key=snd)  # (i, sum(arr[:i])), i in [0, n]
    left, right = None, None
    d_min = inf
    for i, x in a:
        js = set()  # 12 unique indices at most
        for y in (x - k, x + k):  # both +k & -k are attempted as k may be positive or negative
            j = bin_search_left(a, y, key=snd)
            js.update((j - 1, j, j + 1))  # bound on the left, on the insertion point, on the right
            j = bin_search_right(a, y, key=snd)  # considers duplicated values
            js.update((j - 1, j, j + 1))
        for jy in [a[j] for j in js if 0 <= j <= n if i != a[j][0]]:  # j-1 may underflow, j and j+1 may overflow
            p, q = sorted(((i, x), jy))  # tuple sorts lexicographically
            diff = abs(q[1] - p[1] - k)
            if diff < d_min:
                left, right, d_min = p[0], q[0], diff
    return left, right

if __name__ == '__main__':
    from random import randint
    def control(arr, k):  # O(n^3)
        n = len(arr)
        d_min = inf
        for i in range(n):
            for j in range(i, n):
                diff = abs(sum(arr[i:j+1]) - k)
                if diff < d_min:
                    d_min = diff
        return d_min
    for size in range(50):
        for _ in range(size):
            a = [randint(-size, 2 * size) for _ in range(size)]  # 1/3 instances do not have zero-sum subarray
            left, right = search(a)
            assert abs(sum(a[left:right])) == control(a, 0)
            k = randint(-size, size)
            left, right = search_k(a, k)
            assert abs(sum(a[left:right]) - k) == control(a, k), (a, k, left, right, control(a, k))
