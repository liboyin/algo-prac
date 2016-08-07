from math import ceil, log2

class SumTree:  # ref: max_rectangle_under_hist.MinIndexRangeTree
    def __init__(self, arr):  # O(n) time & space
        def build(left, right, i):
            if left == right:
                a[i] = arr[left]
                return a[i]
            mid = (left + right) // 2
            left = build(left, mid, i * 2 + 1)  # recursive call
            right = build(mid + 1, right, i * 2 + 2)  # recursive call
            a[i] = left + right
            return a[i]
        self.n = len(arr)
        h = ceil(log2(self.n))
        a = [None] * (2 * 2 ** h - 1)  # list[num]
        build(0, self.n - 1, 0)
        self.a = a
        self.cache = dict()  # dict[tuple[int,int], num]: query cache

    def get_sum(self, left, right):  # returns sum(arr[left:right+1]). O(\log^h n) time
        def query(sl, sr, i):  # sl: slice left; sr: slice right
            if sr < sl or right < sl or sr < left:
                return 0
            if left <= sl and sr <= right:  # queried range covers the current slice
                return self.a[i]
            mid = (sl + sr) // 2
            q_left = query(sl, mid, i * 2 + 1)  # recursive call
            q_right = query(mid + 1, sr, i * 2 + 2)  # recursive call
            return q_left + q_right
        if (left, right) in self.cache:
            return self.cache[(left, right)]
        r = query(0, self.n - 1, 0)
        self.cache[(left, right)] = r
        return r

def next_geq(arr):  # ref: next_greater.py
    s = [0]
    r = [None] * len(arr)
    for i, x in enumerate(arr[1:], start=1):
        while len(s) > 0 and arr[s[-1]] <= x:
            r[s.pop()] = i
        s.append(i)
    return r

def search(hist):
    def qrs(i, j):  # safely query range sum
        if 0 <= i < n and 0 <= j < n and i <= j:
            return st.get_sum(i, j)
        return 0
    def volume(i):
        j_left = left_geq[i]  # j_left: index of the first geq on the left
        v_left = 0 if j_left is None else (i - j_left - 1) * min(hist[j_left], hist[i]) - qrs(j_left + 1, i - 1)
        # i - j_left - 1: number of gaps between j_left and i (exclusive); qrs(j_left + 1, i - 1): sum(hist[j_left+1:i])
        j_right = right_geq[i]  # j_right: index of the first geq on the right
        v_right = 0 if j_right is None else (j_right - i - 1) * min(hist[j_right], hist[i]) - qrs(i + 1, j_right - 1)
        # j_right - i - 1: number of gaps between i and j_right (exclusive); qrs(i + 1, j_right - 1): sum(hist[i+1:j_right])
        return max(v_left, v_right)
    n = len(hist)
    if n <= 1:
        return 0
    left_geq = next_geq(hist[::-1])
    left_geq.reverse()
    for i, x in enumerate(left_geq):
        if x is not None:
            left_geq[i] = n - 1 - x  # undo reverse for each element
    right_geq = next_geq(hist)  # for all i except i == n - 1, right_geq[i] is not None
    st = SumTree(hist)
    return max(volume(i) for i in range(n))

if __name__ == '__main__':
    from lib import rev_range
    from random import randint
    def control(hist):  # O(n^2)
        max_vol, n = 0, len(hist)
        for i, x in enumerate(hist):
            i_left = next((j for j in rev_range(i) if hist[j] >= x), None)  # index of the first geq on the left
            v_left = 0 if i_left is None else min(x, hist[i_left]) * (i-i_left-1) - sum(hist[i_left+1:i])
            i_right = next((j for j in range(i+1, n) if hist[j] >= x), None)  # index of the first geq on the right
            v_right = 0 if i_right is None else min(x, hist[i_right]) * (i_right-i-1) - sum(hist[i+1:i_right])
            max_vol = max(max_vol, v_left, v_right)
        return max_vol
    for size in range(50):
        a = [randint(0, size) for _ in range(size)]
        assert search(a) == control(a)
