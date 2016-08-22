class FenwickTree:
    """
    adding 1 to index in rev_range(10):
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2]
    [0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2]
    [0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 2]
    [0, 0, 0, 0, 0, 1, 2, 1, 4, 1, 2]
    [0, 0, 0, 0, 1, 1, 2, 1, 5, 1, 2]
    [0, 0, 0, 1, 2, 1, 2, 1, 6, 1, 2]
    [0, 0, 1, 1, 3, 1, 2, 1, 7, 1, 2]
    [0, 1, 2, 1, 4, 1, 2, 1, 8, 1, 2]
    """
    def __init__(self, n):
        assert n > 0
        self.a = [0] * (n + 1)  # bitwise operations require index to start from 1

    def __len__(self):
        return len(self.a) - 1

    def __getitem__(self, i):
        if i == 0:
            return self.a[1]
        return self.sum(i) - self.sum(i - 1)

    def add(self, i, x):
        i += 1
        a = self.a  # shorthand
        assert 0 < i < len(a)
        while i < len(a):  # add forwards
            a[i] += x
            i += i & -i  # adding 1 to the last 1-bit: 5, 6, 8, 16, ...

    def sum(self, i):
        i += 1
        a = self.a  # shorthand
        assert 0 < i < len(a)
        s = 0
        while i > 0:  # sum backwards
            s += a[i]
            i -= i & -i  # zeros the last 1-bit: 7, 6, 4, 0
        return s

    def __repr__(self):
        return str(self.a)

if __name__ == '__main__':
    from random import randint
    for size in range(1, 128):
        ft = FenwickTree(size)
        control = [0] * size
        for _ in range(32):
            i, x = randint(0, size-1), randint(0, 10)
            ft.add(i, x)
            control[i] += x
            for i in range(size):
                assert control[i] == ft[i]
                assert sum(control[:i+1]) == ft.sum(i)
