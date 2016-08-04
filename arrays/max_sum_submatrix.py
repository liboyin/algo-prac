from arrays.max_sum_subarray import search2 as kadane
from itertools import product
from math import inf

def search(mat):
    """
    2D Kadane algorithm: finds the submatrix with the max sum.
    Observation: Consider a max-sum submatrix. Compress it on x-axis, then its starting & ending y-indices are the same
        as in 2D. Likewise, compressing on y-axis, then its starting & ending x-indices are the same as in 2D.
    Time complexity is O(n^3). Space complexity is O(n).
    :param mat: list[list[num]]
    :return:  tuple[int,int,int,int,num]. up, down, left, right coordinate of the submatrix and its sum
    """
    m = len(mat)
    if m == 0:
        return 0
    n = len(mat[0])
    if n == 0:
        return 0
    row_range, col_range, sum_max = None, None, -inf  # bottom & down are inclusive
    for top in range(m):
        a = [0] * n
        for bottom in range(top, m):
            for i, x in enumerate(mat[bottom]):
                a[i] += x
            i, j, s = kadane(a)
            if s > sum_max:
                row_range = top, bottom
                col_range = i, j
                sum_max = s
    return row_range[0], row_range[1], col_range[0], col_range[1], sum_max

def search_k(mat, k):
    """
    Finds the k * k submatrix with the max sum.
    Time complexity is O(n^2). Space complexity is O(n^2).
    :param mat: list[list[num]]
    :param k: int, positive
    :return: tuple[int,int,num]. top-left coordinate of the submatrix and its sum
    """
    def q(i, j):
        if i < 0 or j < 0:
            return 0
        return s[i][j]
    m = len(mat)
    if not 0 < k <= m:
        return 0
    n = len(mat[0])
    if n < k:
        return 0
    s = [[0] * n for _ in range(m)]  # 2d prefix (inclusive) sum matrix
    for i, j in product(range(m), range(n)):
        s[i][j] = mat[i][j] + q(i-1, j) + q(i, j-1) - q(i-1, j-1)  # queried addresses have all been assigned
    i_max, j_max, s_max = -1, -1, -inf
    for i, j in product(range(k-1, m), range(k-1, n)):  # i, j: bottom-right corner of submatrix (inclusive)
        x = s[i][j] - q(i-k, j) - q(i, j-k) + q(i-k, j-k)
        if x > s_max:
            i_max, j_max, s_max = i, j, x
    return i_max-k+1, j_max-k+1, s_max

if __name__ == '__main__':
    from random import randint
    def control(mat):  # O(n^6)
        m, n = len(mat), len(mat[0])
        s_max = -inf
        for ib, jb in product(range(m), range(n)):
            for ie, je in product(range(ib, m), range(jb, n)):  # inclusive finish
                s_max = max(s_max, sum(mat[i][j] for i, j in product(range(ib, ie+1), range(jb, je+1))))
        return s_max
    def control_k(mat, k):  # O(n^2k^2)
        s_max = -inf
        for i, j in product(range(len(mat)-k+1), range(len(mat[0])-k+1)):  # i, j: top-left corner of submatrix
            s_max = max(s_max, sum(mat[i+ii][j+ji] for ii, ji in product(range(k), range(k))))
        return s_max
    assert search(((2, 1, -3, -4, 5), (0, 6, 3, 4, 1), (2, -2, -1, 4, -5), (-3, 3, 1, 0, 3))) == (1, 3, 1, 3, 18)
    for k, v in {(((1, 2, -1, 4), (-8, -3, 4, 2), (3, 8, 10, -8), (-4, -1, 1, 7)), 3): 20,
                 (((-2, 2), (1, -2), (3, -1), (2, -3)), 1): 3}.items():
        assert search_k(*k)[-1] == v
    for size in range(1, 25):
        m = randint(max(1, size-5), size)
        n = randint(max(1, size-5), size)
        k = randint(1, min(m, n))
        a = [[randint(-size, size) for _ in range(n)] for _ in range(m)]
        assert search(a)[-1] == control(a)
        assert search_k(a, k)[-1] == control_k(a, k)
