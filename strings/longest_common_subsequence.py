from arrays.longest_increasing_subsequence import search2 as longest_increasing_subsequence
from lib import rev_enumerate

def search(xs, ys):  # DP with reconstruction. O(mn) time & space
    m, n = len(xs), len(ys)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    bt = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if xs[i] == ys[j]:  # to find the longest repeating subsequence, let xs = ys, and condition i != j here
                dp[i+1][j+1] = dp[i][j] + 1  # bt[i][j] == 0: backtrack to dp[i-1][j-1]
            elif dp[i][j+1] > dp[i+1][j]:
                dp[i+1][j+1] = dp[i][j+1]
                bt[i][j] = -1  # -1: backtrack to dp[i-1][j]
            else:
                dp[i+1][j+1] = dp[i+1][j]
                bt[i][j] = 1  # 1: backtrack to dp[i][j-1]
    r = []
    i, j = m - 1, n - 1
    while i >= 0 and j >= 0:
        if bt[i][j] == 0:
            r.append(xs[i])
            i -= 1
            j -= 1
        elif bt[i][j] == -1:
            i -= 1
        else:  # bt[i][j] == 1
            j -= 1
    return r[::-1]

def search2(xs, ys):
    """
    Finds the longest common subsequence using an O(n\log n) time longest increasing subsequence solution.
    Time complexity is O(n^2). Space complexity is O(n^2). However, most cases should be solved in O(n\log n) time.
    Worst case is when xs and ys are both constant strings of the same char. In this case, the reversed index array
        has length mn; and the length of the LIS is 1.
    :param xs: str
    :param ys: str
    :return: str
    """
    if len(xs) > len(ys):  # build dictionary on the shorter string
        return search2(ys, xs)
    d = dict()  # dict[char, list[int]]. for each char, reversed sequence of occurrence in xs
    for i, x in rev_enumerate(xs):
        if x in d:
            d[x].append(i)
        else:
            d[x] = [i]
    ys1, idx = zip(*[(y, i) for y in ys for i in d.get(y, ())])
    return [ys1[i] for i in longest_increasing_subsequence(idx)]

def is_subsequence_of(sub, arr):
    i = 0  # cursor on arr
    for j in range(len(sub)):
        while i < len(arr) and arr[i] != sub[j]:
            i += 1
        if i == len(arr):
            return False
    return True

if __name__ == '__main__':
    from string import ascii_lowercase as alphabet
    from random import choice
    for _ in range(100):
        xs = [choice(alphabet) for _ in range(100)]
        ys = [choice(alphabet) for _ in range(100)]
        dp = search(xs, ys)
        lis = search2(xs, ys)
        assert len(dp) == len(lis)  # exact subsequence may differ
        assert is_subsequence_of(dp, xs) and is_subsequence_of(dp, ys)
        assert is_subsequence_of(lis, xs) and is_subsequence_of(lis, ys)
