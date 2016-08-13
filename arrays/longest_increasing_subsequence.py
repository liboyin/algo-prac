from bisect import bisect_left
from lib import argmax, bin_search_left, yield_while
from math import inf

def search(arr):  # binary search, length only. O(n\log n) time
    st = [arr[0]]  # st[i]: smallest tail of LIS of length i + 1. naturally sorted, and all elements are distinct
    for x in arr:
        if x > st[-1]:  # if x is greater than the current smallest tail, then no need to search
            st.append(x)
        else:
            st[bisect_left(st, x)] = x  # returns the index of x if in st, or the index of the smallest element larger than x
    return len(st)

def search2(arr):  # binary search with reconstruction. O(n\log n) time, O(n) space
    st = [0]  # st[i]: index (in arr) of the smallest tail of the LIS of length i + 1
    bt = [-1]  # bt[i]: index (in arr) of the predecessor of arr[i] in the LIS so far, or -1 if arr[i] is the head. when finished, len(bt) == len(arr)
    for i, x in enumerate(arr[1:], start=1):
        if x > arr[st[-1]]:  # x is greater than the current smallest tail
            bt.append(st[-1])  # point to the previous element of the current tail of st
            st.append(i)
        else:
            pos = bin_search_left(st, x, key=lambda j: arr[j])
            assert pos < len(st)
            bt.append(st[pos - 1] if pos > 0 else -1)  # pos == 0 -> arr[i] is the new head
            st[pos] = i
    return list(yield_while(st[-1], lambda x: x >= 0, lambda x: bt[x]))[::-1]  # indices only

def search3(arr):  # DP with reconstruction. O(n^2) time, O(n) space
    dp = [1]  # dp[i]: maximum length of increasing subsequence with arr[i] as tail
    bt = [-1]  # bt[i]: index (in arr) of the largest possible predecessor of arr[i], or -1 if arr[i] is the head
    for i, x in enumerate(arr[1:], start=1):
        m = -1  # m: in search for bt[i]
        for j in range(i):
            if arr[j] < x and (m == -1 or dp[j] > dp[m]):
                # among all j < i s.t. arr[j] < arr[i], maximise dp[j]. if multiple such j exist, take the first one
                m = j
        if m == -1:  # arr[i] as the start of dp new increasing subsequence
            dp.append(1)
            bt.append(-1)
        else:
            dp.append(dp[m] + 1)
            bt.append(m)
    return list(yield_while(argmax(dp), lambda s: s >= 0, lambda s: bt[s]))[::-1]  # indices only

def search_triple(arr):  # returns whether a triple i < j < k exists s.t. arr[i] < arr[j] < arr[k]
    fst, snd = inf
    for x in arr:
        if x < fst:
            fst = x
        elif fst < x < snd:
            snd = x
        elif x > snd:
            return True
    return False

if __name__ == '__main__':
    from random import shuffle
    std_test = {(0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15): (0, 4, 6, 9, 13, 15),
                (2, 3, 1, 4, 0, 4, 0, 3, 1, 4, 0): (6, 8, 9)}
    for k, v in std_test.items():
        assert search(k) == len(search2(k)) == len(v)
    for _ in range(100):
        rnd_test = list(range(50)) * 4
        shuffle(rnd_test)
        n = search(rnd_test)
        bs = search2(rnd_test)
        dp = search3(rnd_test)
        assert n == len(bs) == len(dp)
        for i in range(n - 1):
            assert rnd_test[bs[i]] < rnd_test[bs[i + 1]]
            assert rnd_test[dp[i]] < rnd_test[dp[i + 1]]
