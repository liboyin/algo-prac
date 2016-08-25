class DefaultUnionFind2D:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.a = [None] * (m * n)
        self.c = 0

    def ancestor(self, i):
        a = self.a
        assert a[i] is not None
        if a[i] == i:
            return i
        a[i] = self.ancestor(a[i])
        return a[i]

    def is_joint(self, x, y, p, q):
        i = self.n * x + y
        j = self.n * p + q
        a = self.a
        if a[i] is None or a[j] is None:
            return False
        return self.ancestor(i) == self.ancestor(j)

    def try_join(self, x, y, p, q):
        m, n = self.m, self.n
        if not 0 <= x < m or not 0 <= y < n or not 0 <= p < m or not 0 <= q < n:  # if out of range, do nothing
            return
        i, j = n * x + y, n * p + q
        a = self.a
        if a[i] is None or a[j] is None:  # if a[i] or a[j] is unset, do nothing
            return
        i_anc = self.ancestor(i)
        j_anc = self.ancestor(j)
        if i_anc != j_anc:  # if i and j are already joint, do nothing
            a[i_anc] = j_anc
            self.c -= 1

    def set(self, x, y):
        i = self.n * x + y
        a = self.a
        if a[i] is not None:
            return self.c
        a[i] = i
        self.c += 1
        self.try_join(x, y, x - 1, y)
        self.try_join(x, y, x + 1, y)
        self.try_join(x, y, x, y - 1)
        self.try_join(x, y, x, y + 1)
        return self.c
