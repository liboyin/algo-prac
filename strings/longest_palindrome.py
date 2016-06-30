from lib import argmax_2d
from operator import itemgetter as get_item

def search(t):  # DP, O(n^2) time & space
    n = len(t)
    dp = [[-1] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1  # odd length palindromes
    for i in range(1, n):
        dp[i][i-1] = 0  # even length palindromes
    for i in range(1, n-1):
        j = 0
        while j+i < n:
            if t[j] == t[j+i] and dp[j+1][j+i-1] >= 0:
                dp[j][j+i] = dp[j+1][j+i-1] + 2
            j += 1
    i, j = argmax_2d(dp)
    r = []
    while dp[i][j] > 1:  # add mirrored part
        r.append(t[i])
        i += 1
        j -= 1
    if dp[i][j] == 1:
        return ''.join(r + [t[i]] + r[::-1])
    else:  # dp[i][j] == 0
        return ''.join(r + r[::-1])

def search2(text, sep='#'):  # Manacher's algorithm, O(n) time & space
    assert sep not in text
    t = '{0}{1}{0}'.format(sep, sep.join(text))  # TODO: '#' between chars are to handle palindromes of even/odd length. but why boundary '#'?
    mid, right = 0, 0  # mid & right (inclusive) cursor of the longest known palindrome in t
    n = len(t)
    a = [1] * n  # a[i]: width of the longest palindrome centred at t[i], 1 by default in augmented text
    for i in range(n):
        if i < right:  # determine a minimal width. note that mid <= i always holds
            assert a[mid] + mid == right
            a[i] = min(a[2 * mid - i], right - i)  # a[2 * mid - i] == mid - (i - mid), the mirror of i against mid
        while 0 <= i - a[i] and i + a[i] < n and t[i + a[i]] == t[i - a[i]]:  # try larger width
            a[i] += 1
        if i + a[i] > right:
            right = i + a[i]  # this is the only place where right is updated. monotonic increase leads to linear time
            mid = i
    i, m = max(enumerate(a), key=get_item(1))
    return t[i - m + 1: i + m].replace('#', '')  # t[i-(m-1):i+(m-1)+1]. m-1 since a[i] starts from 1

if __name__ == '__main__':
    from string import ascii_lowercase as alphabet
    from random import choice
    for size in range(1, 100):
        rnd_test = ''.join(choice(alphabet) for _ in range(size))
        dp = search(rnd_test)
        manacher = search2(rnd_test)
        assert len(dp) == len(manacher)
