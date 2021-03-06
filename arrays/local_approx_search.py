from collections import OrderedDict

def search(nums, k, t):
    """
    Given an array of integers, returns whether there exists indices i and j, s.t. j - i <= k and abs(arr[i] - arr[j]) <= t.
    Observation: assuming t > 0, abs(arr[i] - arr[j]) <= t -> abs(arr[i] // t - arr[j] // t) <= 1
    Solution is sliding window + OrderedDict, which remembers order of insertion.
    Time complexity is O(n). Space complexity is O(k).
    :param nums: list[int]
    :param k: int, positive
    :param t: int, non-negative
    :return: bool
    """
    assert k > 0 and t >= 0
    t1 = max(1, t)  # generalise t == 0 and t > 0
    d = OrderedDict()  # x // t1 -> x, x in nums
    for i, x in enumerate(nums):
        key = x // t1  # use t1 as key, t for verification
        for y in (key - 1, key, key + 1):
            if y in d and abs(x - d[y]) <= t:
                return True
        if i >= k > 0:  # k == 1 -> start popping from i = 1
            d.popitem(last=False)  # pop the oldest element
        d[key] = x
    return False

if __name__ == '__main__':
    for k, v in {((-1, -1), 1, 0): True,
                 ((1, 3, 1), 1, 1): False,
                 ((2, 0, -2, 2), 2, 1): False}.items():
        assert search(*k) == v
