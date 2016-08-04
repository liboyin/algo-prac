def search(arr, n):
    """
    Given a list of distinct coin values and a total amount. The supply of each kind of coin is sufficient. Returns the
        number of ways the given total amount can be achieved.
    Solution is a variation of 0-1 Knapsack, although the problem looks more like a multi-select Knapsack problem.
    Time complexity is O(mn). Space complexity is O(n).
    :param arr: list[int], positive
    :param n: int, positive
    :return: int, non-negative
    """
    assert n > 0
    assert all(x > 0 for x in arr)
    m = len(arr)
    if m == 0:
        return 0
    dp = [0] * (n+1)  # space-compressed version of an m * n DP table
    # equivalent dp[i][j] denotes the number of ways to achieve amount j using at least one coin of value arr[i]
    dp[0] = 1  # base case
    for x in arr:
        for j in range(n+1):  # unlike 0-1 knapsack, indices are calculated during the iteration
            if dp[j] > 0 and j + x <= n:
                dp[j+x] += dp[j]  # at this moment, dp[j+x] still has the value from the previous iteration.
                # assuming the previous iteration is correct. since at least one arr[i] is being considered, the value
                # of dp[j+arr[i]] after addition is correct. as a base case, the initial table [1,0,0,...] is correct
    return dp[-1]

if __name__ == '__main__':
    from itertools import product
    from random import randint
    def control(arr, n):
        m, c = len(arr), 0
        for xs in product(*[range(n//x+1) for x in arr]):
            c += (sum(arr[i] * xs[i] for i in range(m)) == n)
        return c
    for k, v in {((1, 2, 3, 4), 4): 5,  # {1,1,1,1}, {1,1,2}, {1,3}, {2,2}, {4}
                ((2, 1, 3), 5): 5}.items():  # {1,1,1,1}, {1,1,1,2}, {1,2,2}, {1,1,3}, {2,3}
        if control(*k) != v:
            print(control(*k))
    for _ in range(100):
        a = list({randint(1, 10) for _ in range(5)})
        n = randint(10, 20)
        assert search(a, n) == control(a, n)
