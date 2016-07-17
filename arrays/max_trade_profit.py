from arrays.local_extremas import longest_alternating_subsequence
from lib import rev_range

def search_free(arr):
    """
    Given the price of a stock over n days. Buy & sell are unlimited. Returns the maximum possible profit.
    Solution is to buy in at every local minimum, and sell at every local maximum. Hence equivalent to a longest
    alternating sequence problem. Time complexity is O(n).
    :param arr: list[num]
    :return: num
    """
    las = [arr[i] for i in longest_alternating_subsequence(arr)]
    # alternating sequence of local minimums & maximums. note that:
    # 1. las is locally distinct; 2. las may start with a local max
    if len(las) <= 1 or (len(las) == 2 and las[0] > las[1]):
        return 0
    start = 0 if las[0] < las[1] else 1  # first local minimum
    return sum(las[i+1] - las[i] for i in range(start, len(las)-1, 2))

def search_2(arr):
    """
    Given the price of a stock over n days. Allow at most 2 transactions. Returns the maximum possible profit.
    Observation:
    max_profit = max(for each day i, first sell is <= day i, second buy-in is >= day i)
               = max(for each day i, first sell is on day i, second buy-in is >= day i)
    Note the possibility of selling & buying on day i, which concatenates two transactions into one.
    Solution is a 2-pass scan. Time complexity is O(n).
    :param arr: list[num]
    :return: num
    """
    n = len(arr)
    snd = [0] * n  # snd[i]: max profit of buying in (the 2nd time) >= day i, and selling > day i
    max_after = arr[-1]  # max_after: max(arr[i:])
    for i in rev_range(n-1):
        snd[i] = max(snd[i+1], max_after - arr[i])
        max_after = max(max_after, arr[i])
    fst = [snd[0]]  # it is possible to combine fst and snd, but they are separated here for clarity
    min_before = arr[0]  # min_before: min(arr[:i])
    for i in range(1, n):
        fst.append(max(fst[-1], arr[i] - min_before + snd[i]))
        min_before = min(min_before, arr[i])
    return fst[-1]

def search_k(arr, k):  # at most k transactions. same observation as search_2. O(kn) time & space
    assert k > 0
    n = len(arr)
    dp = [[0] * n for _ in range(k)]  # dp[c][i]: selling on <= day i to complete transaction c+1, maximum total profit
    min_up_to = arr[0]  # min_up_to: min(arr[:i+1])
    for i in range(1, n):  # first transaction
        min_up_to = min(min_up_to, arr[i])
        dp[0][i] = max(dp[0][i - 1], arr[i] - min_up_to)
    for c in range(1, k):
        max_diff = -arr[0]
        for i in range(1, n):
            max_diff = max(max_diff, dp[c-1][i-1] - arr[i-1])  # sold c-1 transaction <= day i-1, bought on day i-1. possible duplication
            dp[c][i] = max(dp[c][i-1], max_diff + arr[i])
    return dp[-1][-1]

if __name__ == '__main__':
    from random import randint
    def control_2(arr):
        m, n = 0, len(arr)
        for i in range(n - 1):
            for j in range(i, n):
                for k in range(j, n-1):
                    for l in range(k, n):
                        m = max(m, arr[j] - arr[i] + arr[l] - arr[k])
        return m
    assert search_free([100, 180, 260, 310, 40, 535, 695]) == 865
    # test search_2
    assert search_2([2, 30, 15, 10, 8, 25, 80]) == 100
    for size in range(2, 20):
        rnd_test = [randint(0, 100) for _ in range(size)]
        assert search_2(rnd_test) == search_k(rnd_test, 2) == control_2(rnd_test)
    # test search_k
    std_test = {((10, 22, 5, 75, 65, 80), 2): 87,
                ((12, 14, 17, 10, 14, 13, 12, 15), 3): 12,
                ((100, 30, 15, 10, 8, 25, 80), 3): 72,
                ((90, 80, 70, 60, 50), 1): 0}
    for k, v in std_test.items():
        assert search_k(*k) == v
