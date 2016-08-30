import numpy as np
import sys

eps = sys.float_info.epsilon

def search(mat):
    """
    Given a matrix in which each cell represents the gain if visited. Returns the maximum gain on a path from the
        top-left corner to the bottom-right corner, moving right or down.
    Solution is DP. Time complexity is O(n^2). Space complexity is O(n^2).
    :param mat: list[list[num]]
    :return: num
    """
    if len(mat) == 0 or len(mat[0]) == 0:  # numpy compatibility
        return 0
    m, n = len(mat), len(mat[0])
    dp = np.ones((m, n), dtype=float) * -inf
    dp[0, 0] = mat[0][0]
    for i in range(m):
        for j in range(n):
            if i + 1 < m:
                dp[i+1, j] = max(dp[i+1, j], dp[i, j] + mat[i+1][j])
            if j + 1 < n:
                dp[i, j+1] = max(dp[i, j+1], dp[i, j] + mat[i][j+1])
    return dp[-1, -1]

if __name__ == '__main__':
    from itertools import product
    from math import inf
    from mathematics.permutation import with_repeat as permute
    from random import randint
    def control(mat):
        m, n = mat.shape
        max_sum = -inf
        for paths in permute([False] * (m - 1) + [True] * (n - 1)):
            i = j = 0
            s = mat[0, 0]
            for x in paths:
                if x:  # n - 1 rightward pointers
                    j += 1
                else:  # m - 1 downward pointers
                    i += 1
                s += mat[i, j]
            max_sum = max(max_sum, s)
        return max_sum
    for m, n in product(range(1, 10), range(1, 10)):
        a = np.random.rand(m, n) * max(m, n) - min(m, n) / 2
        assert abs(control(a) - search(a)) < eps * 10
