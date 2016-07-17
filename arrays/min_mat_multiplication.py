from math import inf

def min_mat_multi(arr):  # O(n^3) time, O(n^2) space
    n = len(arr) - 1  # # of matrices
    dp = [[inf] * n for _ in range(n)]  # dp[i][j]: min operations multiplying matrix i to j, inclusive
    for i in range(n):
        dp[i][i] = 0
    for inc in range(1, n):  # j = i + inc
        i = 0
        while i + inc < n:
            for k in range(i, i+inc):  # connection point. left inclusive, right exclusive
                left, mid, right = arr[i], arr[k+1], arr[i+inc+1]
                # row # of left, col # of left/row # of right, row # of right
                dp[i][i+inc] = min(dp[i][i+inc], dp[i][k] + left*mid*right + dp[k+1][i+inc])
            i += 1
    return dp[0][-1]

if __name__ == '__main__':  # TODO: random test?
    std_test = {(40, 20, 30, 10, 30): 26000,
                (10, 20, 30, 40, 30): 30000,
                (10, 20, 30): 6000}
    for k, v in std_test.items():
        assert min_mat_multi(k) == v
