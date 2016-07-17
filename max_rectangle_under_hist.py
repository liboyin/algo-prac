from math import ceil, inf, log2
from operator import itemgetter as get_item

class MinIndexRangeTree:
    def __init__(self, arr):  # O(n) time & space
        """
        a[i]: (min_idx, min_val) pair in range arr[left:right]. For i = 0, left == 0, right == n.
        a forms an implicit tree. Like a heap, the left child of a[i] is a[2*i+1], representing range arr[left:mid+1],
        where mid == (left + right) // 2; the right child of a[i] is a[2*i+2], representing range arr[mid+1:right].
        Hence, the maximum length is 2 ^ ceil(log2(n) + 1) - 1. Unlike a heap, for all a[i], the left and right subtree
        of a[i] have (almost) identical shape, hence not all cells are used.
        :param arr: list[num]
        """
        def build(left, right, i):
            if left == right:
                a[i] = left, arr[left]  # (min_idx, min_val) pairs
                return a[i]
            mid = (left + right) // 2
            left = build(left, mid, i * 2 + 1)  # recursive call
            right = build(mid + 1, right, i * 2 + 2)  # recursive call
            a[i] = min((left, right), key=get_item(1))
            return a[i]
        self.n = len(arr)
        h = ceil(log2(self.n))  # tree height
        a = [None] * (2 * 2 ** h - 1)  # list[tuple[int, T]]
        build(0, self.n - 1, 0)
        self.a = a
        self.cache = dict()  # dict[tuple[int,int], tuple[int, T]]: query cache

    def get_min(self, left, right):  # returns the min_idx in range arr[left:right+1]. O(\log^h n) time
        def query(sl, sr, i):  # sl: slice left; sr: slice right
            if sr < sl or right < sl or sr < left:
                return None, inf  # for compatibility with type T, replace inf with an infinitely large T instance
            if left <= sl and sr <= right:  # queried range covers the current slice
                # this call either gives the result, or the result will be handled by the upper level
                return self.a[i]
            mid = (sl + sr) // 2
            q_left = query(sl, mid, i * 2 + 1)  # recursive call
            q_right = query(mid + 1, sr, i * 2 + 2)  # recursive call
            return min((q_left, q_right), key=get_item(1))
        if (left, right) in self.cache:
            return self.cache[(left, right)]
        temp = query(0, self.n - 1, 0)[0]  # self.a[0] represents range arr[0:self.n]
        self.cache[(left, right)] = temp
        return temp

def search(hist):
    def query(left, right):
        if left > right:
            return 0  # base case
        if left == right:
            return hist[left]  # base case
        m = rt.get_min(left, right)  # index of the smallest element in hist[left:right+1]
        under = hist[m] * (right - left + 1)
        return max(under, query(left, m - 1), query(m + 1, right))  # recursive call
    rt = MinIndexRangeTree(hist)
    return query(0, len(hist) - 1)

if __name__ == '__main__':
    std_test = {(6, 1, 5, 4, 5, 2, 6): 12}
    for k, v in std_test.items():
        rt = MinIndexRangeTree(k)
        assert search(k) == v
    # [6, 1, 5, 4, 5, 2, 6] -> 12
    # 0-6
    # 0-3/4-6
    # 0-1/2-3/4-5/6
    # 0/1/2/3/4/5/None
