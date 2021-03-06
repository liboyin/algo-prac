from lib import snd
from math import ceil, inf, log2

class MinIndexRangeTree:
    def __init__(self, arr):  # O(n) time & space
        def build(left, right, i):
            if left == right:
                a[i] = left, arr[left]  # (min_idx, min_val) pairs
                return a[i]
            mid = (left + right) // 2  # left: arr[left:mid+1]; right: arr[mid:right+1]
            left = build(left, mid, i * 2 + 1)  # recursive call
            right = build(mid + 1, right, i * 2 + 2)  # recursive call
            a[i] = min((left, right), key=snd)
            return a[i]
        self.n = len(arr)
        h = ceil(log2(self.n))  # h: height of full tree with n nodes. in most cases, not all cells are used
        a = [None] * (2 * 2 ** h - 1)  # 2 * 2 ** h - 1: size of full tree with n leaf nodes and n - 1 internal nodes
        build(0, self.n - 1, 0)  # root corresponds to arr
        self.a = a
        self.cache = dict()  # dict[tuple[int,int], tuple[int, T]]: query cache

    def get_min(self, left, right):  # returns the min_idx in range arr[left:right+1]. O(\log^h n) time
        def query(sl, sr, i):  # sl: slice left; sr: slice right
            if sr < sl or right < sl or sr < left:
                return None, inf
            if left <= sl and sr <= right:  # queried range covers the current slice
                return self.a[i]  # returns a partial result except for the first function call
            mid = (sl + sr) // 2
            q_left = query(sl, mid, i * 2 + 1)  # recursive call
            q_right = query(mid + 1, sr, i * 2 + 2)  # recursive call
            return min((q_left, q_right), key=snd)
        if (left, right) in self.cache:
            return self.cache[(left, right)]
        r = query(0, self.n - 1, 0)[0]  # self.a[0] represents range arr[0:self.n]
        self.cache[(left, right)] = r
        return r

def search(hist):  # O(n\log^d n) time, O(n) space
    def query(left, right):
        if left > right:
            return 0  # base case
        m = rt.get_min(left, right)  # index of the smallest element in hist[left:right+1]
        return max(hist[m] * (right - left + 1), query(left, m - 1), query(m + 1, right))  # recursive call
    if not hist:
        return 0
    rt = MinIndexRangeTree(hist)
    return query(0, len(hist) - 1)

def search2(hist):  # O(n) time, O(n) space TODO: review
    if not hist:
        return 0
    max_area = 0
    s = []  # stack of indices of an increasing subsequence
    for i, x in enumerate(hist + [0]):  # seal right end
        while s and hist[s[-1]] > x:
            h = hist[s.pop()]
            max_area = max(max_area, h * ((i - s[-1] - 1) if s else i))
            # if 0 exists in the middle of hist, height would be 0 when it's encountered again
        s.append(i)
    return max_area

if __name__ == '__main__':
    from lib import rev_range
    from random import randint
    def control(hist):  # O(n^2)
        max_rec, n = 0, len(hist)
        for i, x in enumerate(hist):
            left = next((j for j in rev_range(i) if hist[j] < x), -1)
            right = next((j for j in range(i+1, n) if hist[j] < x), n)
            max_rec = max(max_rec, x * (right - left - 1))
        return max_rec
    for k, v in {(6, 1, 5, 4, 5, 2, 6): 12}.items():
        assert search(k) == search2(list(k)) == v
    for size in [x for x in range(50) for _ in range(x)]:
        a = [randint(0, size) for _ in range(size)]
        assert search(a) == search2(a) == control(a)
