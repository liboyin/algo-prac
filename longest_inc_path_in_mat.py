import numpy as np

def search(mat):
    """
    Finds the length of the longest increasing path in a matrix.
    Time complexity is O(n^2). Space complexity is O(n^2).
    :param mat: list[list[num]]
    :return: int
    """
    def query(i, j, d_to):
        if not (0 <= i < m and 0 <= j < n):  # invalid location
            return 0
        if dp[i][j][d_to] > 0:  # already explored
            return dp[i][j][d_to]
        i_to, j_to = i + dirs[d_to][0], j + dirs[d_to][1]
        if not (0 <= i_to < m and 0 <= j_to < n):  # invalid target
            dp[i][j][d_to] = 1
            return 1
        if mat[i_to][j_to] - mat[i][j] > 0:  # modify here to change the path property
            x = 1 + max([query(i_to, j_to, d) for d in range(4) if d != 3 - d_to])
            # recursive call to all 3 directions except for coming back
            dp[i][j][d_to] = x
            return x
        else:  # function call shall not pass
            dp[i][j][d_to] = 1
            return 1
    dirs = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # left, up, down, right
    m = len(mat)
    if m == 0:
        return 0
    n = len(mat[0])
    dp = np.zeros((m, n, 4), dtype=int)
    max_size = 1
    for i in range(m):
        for j in range(n):
            for d in range(4):
                max_size = max(max_size, query(i, j, d))
    return max_size

if __name__ == '__main__':
    std_test = {((1, 2, 9), (5, 3, 8), (4, 6, 7)): 7,
                ((3, 2, 5), (4, 1, 4), (5, 6, 5)): 6,
                ((9, 9, 4), (6, 6, 8), (2, 1, 1)): 4}
    for k, v in std_test.items():
        assert search(k) == v
