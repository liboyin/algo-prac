from math import ceil, inf, log2

class SumTree:
    def __init__(self, arr):  # O(n) time & space
        """
        a[i]: sum(arr[left:right]). For i = 0, left == 0, right == n.
        a forms an implicit tree. Like a heap, the left child of a[i] is a[2*i+1], representing range arr[left:mid+1],
        where mid == (left + right) // 2; the right child of a[i] is a[2*i+2], representing range arr[mid+1:right].
        Hence, the maximum length is 2 ^ ceil(log2(n) + 1) - 1. Unlike a heap, for all a[i], the left and right subtree
        of a[i] have (almost) identical shape, hence not all cells are used.
        :param arr: list[num]
        """
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
        h = ceil(log2(self.n))  # tree height
        a = [None] * (2 * 2 ** h - 1)  # list[num]
        build(0, self.n - 1, 0)
        self.a = a
        self.cache = dict()  # dict[tuple[int,int], num]: query cache

    def get_sum(self, left, right):  # returns sum(arr[left:right+1]). O(\log^h n) time
        def query(sl, sr, i):  # sl: slice left; sr: slice right
            if sr < sl or right < sl or sr < left:
                return -inf  # for compatibility with type T, replace inf with an infinitely small T instance
            if left <= sl and sr <= right:  # queried range covers the current slice
                # this call either gives the result, or the result will be handled by the upper level
                return self.a[i]
            mid = (sl + sr) // 2
            q_left = query(sl, mid, i * 2 + 1)  # recursive call
            q_right = query(mid + 1, sr, i * 2 + 2)  # recursive call
            return q_left + q_right
        if (left, right) in self.cache:
            return self.cache[(left, right)]
        temp = query(0, self.n - 1, 0)
        self.cache[(left, right)] = temp
        return temp

def next_geq(arr):
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
        j = left_geq[i]  # j: index of the left geq
        left = 0 if j is None else (i-j) * min(hist[j], hist[i]) - qrs(j + 1, i - 1)
        j = right_geq[i]  # j: index of the right geq
        right = 0 if j is None else (j-i) * min(hist[j], hist[i]) - qrs(i + 1, j - 1)
        return max(left, right)
    n = len(hist)
    if n <= 1:
        return 0
    left_geq = next_geq(hist[::-1])
    left_geq.reverse()
    for i, x in enumerate(left_geq):
        if x is not None:
            left_geq[i] = n - 1 - x
    right_geq = next_geq(hist)
    st = SumTree(hist)
    return max(volume(i) for i in range(n))

if __name__ == '__main__':  # TODO: random test?
    print(search([1, 2, 1]))
