def first_kind(n, k):
    """
    Denote by S(n, k) the number of ways n elements can be arranged as k non-empty permutations.
    Recursively, S(n + 1, k) = S(n, k - 1) + n * S(n, k), where S(n, k - 1) creates a new permutation for the current
        element, and n * S(n, k) inserts the current element to the left of any element in existing permutations.
    Base case: S(x, x) = 1, where x >= 0; S(x, 0) = 0, where x >= 1.
    :param n: int, non-negative
    :param k: int, non-negative
    :return: int
    """
    if n == k:
        return 1
    if k == 0:
        return 0
    dp = [[0] * (k+1) for _ in range(n+1)]
    for i in range(k + 1):  # n >= k
        dp[i][i] = 1
    for i in range(2, n+1):
        for j in range(1, min(i, k+1)):
            dp[i][j] = dp[i - 1][j - 1] + (i - 1) * dp[i - 1][j]
    return dp[-1][-1]

def second_kind(n, k):
    """
    Denote by S(n, k) the number of ways n elements can be arranged as k non-empty sets.
    Recursively, S(n + 1, k) = S(n, k - 1) + k * S(n, k), where S(n, k - 1) creates a new set for the current element,
        and k * S(n, k) inserts the current element to any existing sets.
    Base case: S(x, x) = 1, where x >= 0; S(x, 0) = 0, where x >= 1.
    :param n: int, non-negative
    :param k: int, non-negative
    :return: int
    """
    if n == k:
        return 1
    if k == 0:
        return 0
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(k + 1):  # n >= k
        dp[i][i] = 1
    for i in range(2, n + 1):
        for j in range(1, min(i, k + 1)):
            dp[i][j] = dp[i - 1][j - 1] + j * dp[i - 1][j]
    return dp[-1][-1]

if __name__ == '__main__':
    def control1(n, k):
        if n == k:
            return 1
        if k == 0:
            return 0
        return control1(n - 1, k - 1) + (n - 1) * control1(n - 1, k)
    def control2(n, k):
        if n == k:
            return 1
        if k == 0:
            return 0
        return control2(n - 1, k - 1) + k * control2(n - 1, k)
    for n in range(10):
        for k in range(n + 1):
            assert first_kind(n, k) == control1(n, k)
            assert second_kind(n, k) == control2(n, k)
