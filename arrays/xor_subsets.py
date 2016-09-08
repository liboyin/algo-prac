from lib import filter_index
from math import floor, log2

def search(arr, k):
    """
    Given an int array and int k, returns the number of non-empty subsets of arr having XOR of elements as k.
    Observation: XOR of any subset is capped by the greatest integer that can be represented using the # of effective
        bits of the maximum element. Denote this integer by c.
    Solution is based on classic 0-1 Knapsack. Time complexity is O(cn). Space complexity is O(cn).
    :param arr: list[int], non-negative. max element must be positive
    :param k: int, non-negative
    :return: int
    """
    assert k >= 0
    if not arr:
        return 0
    dp = [0] * (2 ** (floor(log2(max(arr))) + 1))  # [0] * (c + 1)
    dp[0] = dp[arr[0]] = 1
    for i, x in enumerate(arr[1:], start=1):
        dp1 = list(dp)
        for j in filter_index(lambda y: y > 0, dp):
            dp1[j^x] += dp[j]
        dp = dp1
    return dp[0] - 1 if k == 0 else dp[k]  # selecting 0 element is not valid

if __name__ == '__main__':
    from functools import reduce
    from itertools import compress, product
    from operator import xor
    from random import randint
    def control(arr, k):
        c = 0
        for mask in product(*([(0, 1)] * len(arr))):
            c += reduce(xor, compress(arr, mask), 0) == k
        return c - 1 if k == 0 else c
    for k, v in {((6, 9, 4, 2), 6): 2,
                 ((1, 2, 3, 4, 5), 4): 4}.items():
        assert search(*k) == v
    for size in [x for x in range(15) for _ in range(x)]:
        a = [randint(1, size) for _ in range(size)]
        k = randint(0, size // 2)
        assert search(a, k) == control(a, k)
