from math import inf

def search(xs, ys):
    """
    Finds the Levenshtein distance between two strings. Insertion, deletion and alteration are allowed.
    Wagner–Fischer algorithm. Time complexity is O(mn). Space complexity is O(mn).
    :param xs: str
    :param ys: str
    :return: int
    """
    m, n = len(xs), len(ys)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for i in range(n+1):
        dp[0][i] = i
    for i in range(1, m+1):
        for j in range(1, n+1):
            if xs[i-1] == ys[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[-1][-1]

def search2(xs, ys):  # O(min(m, n)) space by iterating through rows of DP table
    m, n = len(xs), len(ys)
    if m < n:
        return search2(ys, xs)
    a = list(range(n+1))
    for i in range(m):
        a1 = [i+1] * (n+1)
        for j in range(1, n+1):
            if xs[i] == ys[j-1]:
                a1[j] = a[j-1]
            else:
                a1[j] = 1 + min(a[j], a1[j-1], a[j-1])
        a = a1
    return a[-1]

def is_k_palindrome(t, k):
    """
    Finds whether t is palindromic after removing at most k chars.
    Observation: Equivalent to finding whether the edit distance between t and t.reverse() is smaller than or equal to
        2 * k. Note that this is not Levenshtein distance, in that only insertion and deletion are allowed.
    It is only necessary to explore within radius k around the diagonal. Hence, time complexity is O(nk). Space
        complexity is O(mn) in this implementation, but can be optimised to O(min(m, n)).
    :param t: str
    :param k: str
    :return: bool
    """
    n = len(t)
    dp = [[inf] * (n+1) for _ in range(n+1)]
    for i in range(k+1):
        dp[0][i] = dp[i][0] = i
    tr = t[::-1]
    for i in range(n):
        for j in range(max(0, i-k), min(i+k, n)):  # hence O(nk) time
            if t[i] == tr[j]:
                dp[i+1][j+1] = dp[i][j]
            else:
                dp[i+1][j+1] = min(dp[i+1][j], dp[i][j+1]) + 1  # dp[i+1][j] may be uninitialised, hence requiring inf as default
    return dp[-1][-1] <= k * 2

if __name__ == '__main__':
    print(search('sitting', 'kitten'))
    print(search2('sitting', 'kitten'))
    assert is_k_palindrome('acdcb', 2)
    assert is_k_palindrome('matdam', 1)
    assert not is_k_palindrome('abdxa', 1)
