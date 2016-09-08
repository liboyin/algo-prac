from lib import filter_index, identity, rev_range
from math import ceil, floor

def search(arr, k):
    """
    Returns whether the given array can be rearranged into two subsequences a and b, s.t. |sum(a) - sum(b)| <= k.
    Solution is classic 0-1 knapsack DP. Time complexity is O(n^2). Space complexity is O(s), where s = sum(arr).
    :param arr: list[int]
    :param k: int
    :return: bool
    """
    if k < 0:
        return search(arr, -k)
    s = sum(arr)
    assert 0 <= s / 2 - k <= s / 2 + k
    dp = [False] * (s // 2 + k + 1)
    dp[0] = True
    for x in arr:
        for i in list(filter_index(identity, dp)):  # indices must be obtained before modification
            if i + x < len(dp):
                dp[i+x] = True
    return any(dp[ceil(s/2-k): floor(s/2+k)+1])  # higher range out of bound is handled automatically

def search2(arr):
    """
    Returns a partition, represented as two subsequences a and b, s.t. |sum(a) - sum(b)| is minimised.
    Solution is classic 0-1 knapsack DP. Time complexity is O(n^2). Space complexity is O(s), where s = sum(arr).
    :param arr: list[int], non-negative
    :return: tuple[list[int],list[int]]
    """
    n, s = len(arr), sum(arr)
    if n == 0:
        return [], []
    dp = [None] * (s + 1)
    dp[0] = [0] * n  # bit array for elements in arr
    for i, x in enumerate(arr):
        for j in list(filter_index(lambda x: x is not None, dp)):  # indices must be obtained before modification
            if j + x < s + 1 and dp[j+x] is None:
                dp[j+x] = list(dp[j])
                dp[j+x][i] = 1
    left_ix = next(((i, dp[i]) for i in rev_range(ceil(s/2)) if dp[i] is not None), None)
    right_ix = next(((i, dp[i]) for i in range(ceil(s/2), s+1) if dp[i] is not None), None)
    if left_ix is None:
        selected = right_ix[1]
    elif right_ix is None:
        selected = left_ix[1]
    else:
        selected = min(left_ix, right_ix, key=lambda x: abs(x[0]-s/2))[1]
    left, right = [], []
    for i in range(n):
        if selected[i]:
            left.append(arr[i])
        else:
            right.append(arr[i])
    return left, right

if __name__ == '__main__':
    from itertools import product
    from math import inf
    from random import randint
    def control(arr):
        n, m = len(arr), inf
        for xs in product(*([(0, 1)] * n)):
            ls = sum(y for x, y in zip(xs, arr) if x)
            rs = sum(y for x, y in zip(xs, arr) if not x)
            m = min(m, abs(ls - rs))
        return 0 if n == 0 else m
    for size in [x for x in range(15) for _ in range(x)]:
        a = [randint(0, size) for _ in range(size)]
        ls, rs = search2(a)
        assert abs(sum(ls) - sum(rs)) == control(a)
