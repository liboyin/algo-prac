import numpy as np
from itertools import product
from lib import yield_while

class FenwickTree2D:
    @staticmethod
    def from_mat(a):
        m, n = len(a), len(a[0])
        ft = FenwickTree2D(m, n)
        for i in range(m):
            for j, x in enumerate(a[i]):
                ft.add(i, j, x)
        return ft

    def __init__(self, m, n):
        """
        2D version of Fenwick sum tree. Rows & columns operate independently.
        Time complexity is O(\log m \log n). Space complexity is O(mn).
        :param m: int
        :param n: int
        """
        self.a = np.zeros((m + 1, n + 1), dtype=int)

    def shape(self):
        m, n = self.a.shape
        return m - 1, n - 1

    def add(self, i, j, x):
        a = self.a
        i += 1
        j += 1
        m, n = a.shape
        assert 0 < i < m and 0 < j < n
        ps = yield_while(i, lambda x: x < m, lambda x: x + (x & -x))
        qs = yield_while(j, lambda x: x < n, lambda x: x + (x & -x))
        for p, q in product(ps, qs):
            a[p, q] += x

    def query(self, i, j):
        a = self.a
        i += 1
        j += 1
        m, n = a.shape
        if i * j == 0:
            return 0
        assert 0 < i < m and 0 < j < n
        s = 0
        ps = yield_while(i, lambda x: x > 0, lambda x: x - (x & -x))
        qs = yield_while(j, lambda x: x > 0, lambda x: x - (x & -x))
        for p, q in product(ps, qs):
            s += a[p, q]
        return s

    def query_range(self, i1, j1, i2, j2):
        return self.query(i2, j2) - self.query(i2, j1-1) - self.query(i1-1, j2) + self.query(i1-1, j1-1)

    def __repr__(self):
        return str(self.a[1:, 1:])

if __name__ == '__main__':
    from random import randint
    a = [[3, 0, 1, 4, 2],
         [5, 6, 3, 2, 1],
         [1, 2, 0, 1, 5],
         [4, 1, 0, 1, 7],
         [1, 0, 3, 0, 5]]
    ft = FenwickTree2D.from_mat(a)
    assert ft.query_range(2, 1, 4, 3) == 8
    ft.add(3, 2, 2)
    assert ft.query_range(2, 1, 4, 3) == 10
    for _ in range(10):
        m = randint(1, 16)
        n = randint(1, 16)
        a = np.zeros((m, n), dtype=int)
        ft = FenwickTree2D(m, n)
        for _ in range(1000):
            i = randint(0, m-1)
            j = randint(0, n-1)
            x = randint(-100, 100)
            a[i, j] += x
            ft.add(i, j, x)
            for i, j in product(range(m), range(n)):
                assert ft.query(i, j) == a[:i+1, :j+1].sum()
