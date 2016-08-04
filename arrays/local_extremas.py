from math import inf

def all_local_max(arr):
    """
    A local max satisfies arr[i-1] < arr[i] > arr[i+1], for 1 <= i < n-1. For 0 and n-1, consider one side only.
    Returns a generator of indices of all local max in arr.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[num]
    :return: generator[int]
    """
    def q(i):
        if 0 <= i < len(arr):
            return arr[i]
        return -inf
    return filter(lambda i: q(i-1) < q(i) > q(i+1), range(len(arr)))

def any_local_max(arr):
    """
    At least one local max exist iff arr is pairwise distinct. (Note that asserting so requires linear time.)
    If multiple local max exist, there is no guarantee on which one is returned.
    Time complexity is O(\log n). Space complexity is O(1).
    :param arr: list[num]. must be locally distinct, unless len(arr) == 1
    :return: int
    """
    def q(i):
        if 0 <= i < len(arr):
            return arr[i]
        return -inf
    assert len(arr) > 0
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        # binary search cannot handle repetitions. consider [1, 5, 2, 2, 2, 2, 1]
        if q(mid - 1) < q(mid) > q(mid + 1):  # mid is a local max
            return mid
        elif q(mid - 1) < q(mid) < q(mid + 1):  # monotonically increasing
            left = mid + 1
        else:  # mid is a local min, or monotonically decreasing
            right = mid - 1
    return left

def longest_alternating_subsequence(arr):
    """
    A local min satisfies arr[i-1] > arr[i] < arr[i+1], for 1 <= i < n-1. For 0 and n-1, consider one side only.
    Returns a list of indices of all local min & max in arr. Note that a local min is always followed by a local max,
        and vice versa. Hence, such a list is also the longest alternating subsequence of arr.
    Time complexity is O(n). Space complexity is O(n).
    :param arr: list[num]
    :return: list[int]
    """
    n = len(arr)
    if n == 0:
        return []
    if n == 1:
        return [arr[0]]
    las = []
    if arr[0] != arr[1]:
        las.append(0)
    for i in range(1, n - 1):
        if (arr[i-1] - arr[i]) * (arr[i] - arr[i+1]) < 0:
            las.append(i)
    if arr[-1] != arr[las[-1]]:
        # las is necessarily non-empty here. if las[-1] is a local min, and arr[-1] < arr[las[-1]], then either there is
        # a local max between them, or las[-1] is not a local min. same contradiction holds if las[-1] is a local max
        las.append(n - 1)
    return las

if __name__ == '__main__':  # for problems on local min/max, take extra care on repetitions
    from lib import remove_duplicates
    from random import randint
    for _ in range(1000):
        def q(i):
            if 0 <= i < len(a):
                return a[i]
            return -inf
        a = list(remove_duplicates(randint(-100, 100) for _ in range(100)))
        any_lm = any_local_max(a)
        all_lm = list(all_local_max(a))
        las = longest_alternating_subsequence(a)
        assert any_lm in all_lm
        assert any_lm in las
        for i in all_lm:
            assert i in las
            assert q(i - 1) < q(i) > q(i + 1)
