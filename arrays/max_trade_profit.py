from math import inf
from lib import rev_range

def search_free(arr):
    """
    Given the price of a stock over n days. Buy & sell are unlimited. Returns the maximum possible profit.
    Solution is greedy. Time complexity is O(n). Space complexity is O(1).
    :param arr: list[num]
    :return: num
    """
    n = len(arr)
    if n <= 1:
        return 0
    s = 0
    for i in range(1, n):
        if arr[i-1] < arr[i]:
            s += arr[i] - arr[i-1]
    return s

def search2(arr):
    """
    Given the price of a stock over n days. Allow at most 2 transactions. Returns the maximum possible profit.
    Observation:
    max_profit = max(for each day i, first sell is <= day i, second buy-in is >= day i)
               = max(for each day i, first sell is on day i, second buy-in is >= day i)
    Note the possibility of selling & buying on day i, which merges two transactions.
    Solution is a 2-pass scan. Time complexity is O(n). Space complexity is O(n).
    :param arr: list[num]
    :return: num
    """
    n = len(arr)
    if n <= 1:
        return 0
    pre_min = arr[0]
    fst = [0]  # fst[i]: maximum profit trading at most, considering arr[:i+1]
    for x in arr[1:]:
        pre_min = min(x, pre_min)
        fst.append(max(fst[-1], x - pre_min))
    profit = 0
    post_max = arr[-1]
    for i in rev_range(n):
        post_max = max(arr[i], post_max)
        profit = max(profit, post_max - arr[i] + fst[i])
    return profit

def search2_2(arr):
    hold1 = hold2 = -inf  # profit after buying in the 1st and 2nd time
    release1 = release2 = 0  # profit after selling out the 1st and 2nd time
    for x in arr:
        release2 = max(release2, hold2 + x)
        hold2 = max(hold2, release1 - x)
        release1 = max(release1, hold1 + x)
        hold1 = max(hold1, -x)
    return release2

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

def search_k2(arr, k):
    n = len(arr)
    if n <= 1 or k == 0:
        return 0
    simple = []  # local min & max
    inc = False  # whether x is in an increasing subarray
    for i in range(1, n):
        if arr[i] > arr[i-1] and not inc:  # i-1 is a local min
            inc = True
            simple.append(arr[i-1])
        if arr[i] < arr[i-1] and inc:  # i-1 is a local max
            inc = False
            simple.append(arr[i-1])
    if inc:  # the last element is in an increasing subarray
        simple.append(arr[-1])
    n = len(simple)
    if k >= n // 2:  # at most n // 2 transactions are possible
        return sum(max(0, y - x) for x, y in zip(simple, simple[1:]))
    hold = [-inf] * k
    release = [0] * k
    for x in simple:
        last = 0
        for i in range(k):
            hold[i] = max(hold[i], last - x)
            release[i] = max(release[i], hold[i] + x)
            last = release[i]
    return release[-1]

def search4(arr):  # one day cooldown after sell
    release = 0  # free to buy
    hold = cool = -inf  # hold: have not sold; cool: just sold
    for x in arr:
        release, hold, cool = max(release, cool), max(hold, release - x), hold + x  # takes effect in the next iteration
    return max(release, cool)

if __name__ == '__main__':
    from random import randint
    def control_2(arr):  # O(n^4)
        m, n = 0, len(arr)
        for i in range(n):
            for j in range(i, n):
                for k in range(j, n):
                    for l in range(k, n):
                        m = max(m, arr[j] - arr[i] + arr[l] - arr[k])
        return m
    assert search_free([100, 180, 260, 310, 40, 535, 695]) == 865
    # test search2
    for k, v in {(2, 30, 15, 10, 8, 25, 80): 100}.items():
        assert search2(k) == search2_2(k) == v
    for size in [x for x in range(2, 25) for _ in range(x)]:
        a = [randint(0, size * 2) for _ in range(size)]
        assert search2(a) == search_k(a, 2) == search_k2(a, 2) == control_2(a)
    # test search_k
    for k, v in {((10, 22, 5, 75, 65, 80), 2): 87,
                 ((12, 14, 17, 10, 14, 13, 12, 15), 3): 12,
                 ((100, 30, 15, 10, 8, 25, 80), 3): 72,
                 ((90, 80, 70, 60, 50), 1): 0}.items():
        assert search_k(*k) == search_k2(*k) == v
