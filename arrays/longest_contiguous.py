def subarray(arr):
    """
    A contiguous subarray of an int array contains all integers from min(sub) to max(sub), inclusive.
    Returns the starting and ending (exclusive) index of the longest contiguous subarray.
    Expected time complexity is O(n^2). Space complexity is O(n).
    It is further possible to reduce the time complexity to O(n\log^2 n) by sliding a variable-size window over arr,
        whose size is binary searched. To allow min & max query on the window, it has to be implemented as a tree.
    :param arr: list[int]
    :return: tuple[int,int]
    """
    n = len(arr)
    assert n > 0
    left, right = 0, 0
    for i in range(n):
        s = {arr[i]}
        s_min = s_max = arr[i]
        j = i + 1
        while j < n and arr[j] not in s:  # a contiguous subarray cannot contain duplicates
            s.add(arr[j])
            s_min = min(arr[j], s_min)
            s_max = max(arr[j], s_max)
            if s_max - s_min == j - i and j - i > right - left:
                left, right = i, j
            j += 1
    return left, right + 1

def subsequence(arr):
    """
    Returns the length of the longest contiguous subsequence. e.g. f([3, 6, 2, 7, 1]) = 3 for [3, 2, 1]
    Expected time complexity is O(n). Space complexity is O(n).
    :param arr: list[int]
    :return: int
    """
    def reach(x):
        if x - 1 in s:
            return -1
        i = 1
        while x + i in arr:
            i += 1
        return i
    if not arr:
        return 0
    s = set(arr)
    return max(map(reach, arr))

def subsequence2(arr):  # not as elegant, but same time complexity
    assert len(arr) == len(set(arr))  # requires unique elements
    d = dict()  # dict[int,tuple[int,int]]. x -> min & max element of the longest range containing x
    for x in arr:  # note that in all 4 cases, only edges need update, hence linear time
        if x - 1 in d:
            left = d[x-1][0]
            if x + 1 in d:  # case 1: x joins two ranges
                right = d[x+1][1]
                d[left] = d[right] = left, right
            else:  # case 2: x is the new right
                d[left] = d[x] = left, x
        elif x + 1 in d:  # case 3: x is the new left
            right = d[x+1][1]
            d[x] = d[right] = x, right
        else:  # case 4: x is a new range by itself
            d[x] = x, x
    return max(right - left + 1 for left, right in d.values())

def increasing_subsequence(arr):
    """
    Returns the length of the longest contiguously increasing subsequence. e.g. f([4, 3, 1, 2]) = 2 for [1, 2].
    Solution is DP. Expected time complexity is O(n). Space complexity is O(n).
    :param arr: list[int]
    :return: int
    """
    if not arr:
        return 0
    dp = [1] * len(arr)  # dp[i]: length of the longest CIS ending with arr[i]
    d = dict()  # x -> index of last occurrence of x in arr[:i]
    for i, x in enumerate(arr):
        if x - 1 in d:
            dp[i] = dp[d[x-1]] + 1
        d[x] = i
    return max(dp)

if __name__ == '__main__':
    from itertools import compress, product
    from lib import is_sorted, rev_range, sliding_window
    from random import randint
    def control_subarray(arr):  # O(n^3)
        def step(n):
            for win in sliding_window(arr, n):
                s = set(win)
                if len(s) == n and max(s) - min(s) == n - 1:
                    return True
            return False
        return next(i for i in rev_range(len(arr) + 1) if step(i))
    def control_subsequence(arr, inc=False):  # O(n 2^n)
        m = 0
        for mask in product(*([(0, 1)] * len(arr))):
            sub = list(compress(arr, mask))
            if not sub or (inc and not is_sorted(sub)):
                continue
            if len(sub) == len(set(sub)) and max(sub) - min(sub) == len(sub) - 1:
                m = max(m, mask.count(1))
        return m
    for size in [x for x in range(10, 20) for _ in range(x)]:
        a = [randint(0, size // 5) for _ in range(size)]
        left, right = subarray(a)
        s = set(a[left:right])
        assert len(s) == control_subarray(a)
        assert max(s) - min(s) == len(s) - 1
    for size in [x for x in range(15) for _ in range(x)]:
        a = [randint(0, size // 2) for _ in range(size)]
        assert subsequence(a) == control_subsequence(a)
        assert increasing_subsequence(a) == control_subsequence(a, inc=True)
