from lib import filter_index
from operator import not_

def search(arr, k):
    """
    Given a bool array, flip at most k 0s to 1s. Returns the maximum number of consecutive 1s.
    Solution is sliding window. Time complexity is O(n). Space complexity is O(n).
    :param arr: list[bool]
    :param k: int, positive
    :return: int, non-negative
    """
    n = len(arr)
    if n == 0:
        return 0
    zeros = list(filter_index(not_, arr))  # indices of zeros in arr
    m = len(zeros)
    if m <= k:  # all zeros should be flipped
        return n
    if m == n:  # zero array
        return k
    if m == 0:  # one array
        return n
    # slide a window of size k on zeros
    zeros = [-1] + zeros + [n]
    max_len = 0
    for i in range(1, m + 2 - k):
        left = zeros[i-1] + 1  # index of the first 1 on the left
        right = zeros[i+k] - 1  # index of the first 1 on the right
        max_len = max(max_len, right - left + 1)
    return max_len

if __name__ == '__main__':
    import re
    from itertools import combinations
    def control(arr, k):  # O(2^n)
        def step(flip):
            new = list(arr)
            for i in flip:
                new[i] = 1
            return len(max(re.compile('1+').findall(''.join(map(str, new)))))  # substrings '1+' are sorted by length
        zeros = list(filter_index(not_, arr))
        if len(zeros) <= k:
            return len(arr)
        return max(step(xs) for xs in combinations(zeros, k))  # all subsets with with size k
    for k, v in {((1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1), 2): 8,  # flip [5, 7]
                 ((1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1), 1): 5,  # flip [7]
                 ((0, 0, 0, 1), 4): 4}.items():  # flip [0, 1, 2]
        assert control(*k) == v
    # arr = [1,0,0,1,1,0,1,0,1,1,1]; zeros = [-1,1,2,5,7,11]
    # query: for each i, index (in arr) of the first 1 on the left and on the right?
    # 1: (0, 1)
    # 2: (2, 4)
    # 5: (3, 6)
    # 7: (6, 10)
