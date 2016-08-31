from lib import argmax, identity, rev_range
from math import ceil, log2

class MinMaxHeap:
    """
    Min-Max Heap property:
    1. An element on even layer is less than or equal to its descendants.
    2. An element on odd layer is greater than or equal to its descendants.
    3. Root is on layer 0.
    ref: Min-Max Heaps and Generalized Priority Queues, Atkinson et al., ACM Communications, Oct 1986
    """
    @staticmethod
    def min_layer(i):
        return not int(log2(i+1)) & 1

    def __init__(self, iterable, key=identity):  # key: T -> comparable
        self.a = list(iterable)
        self.key = key
        self.heapify()

    def __len__(self):
        return len(self.a)

    def bubble_up(self, i):
        if i == 0:
            return
        a, f = self.a, self.key  # shorthand
        j = (i - 1) // 2  # parent of i
        if self.min_layer(i):
            if f(a[i]) > f(a[j]):  # max heap property at j is violated
                a[i], a[j] = a[j], a[i]  # Pythonic swap
                self.bubble_up_max(j)
            else:
                self.bubble_up_min(i)
        else:  # i is on max layer
            if f(a[i]) < f(a[j]):  # min heap property at j is violated
                a[i], a[j] = a[j], a[i]
                self.bubble_up_min(j)
            else:
                self.bubble_up_max(i)

    def bubble_up_min(self, i):  # i is on min layer
        if int(log2(i+1)) <= 1:
            return
        a, f = self.a, self.key
        j = ((i - 1) // 2 - 1) // 2  # grandparent of i
        if f(a[i]) < f(a[j]):
            a[i], a[j] = a[j], a[i]  # after the swap, min heap property at i is intact
            self.bubble_up_min(j)

    def bubble_up_max(self, i):  # i is on max layer
        if int(log2(i + 1)) <= 1:
            return
        a, f = self.a, self.key
        j = ((i - 1) // 2 - 1) // 2
        if f(a[i]) > f(a[j]):
            a[i], a[j] = a[j], a[i]  # after the swap, min heap property at i is intact
            self.bubble_up_max(j)

    def trickle_down(self, i):
        if self.min_layer(i):
            self.trickle_down_min(i)
        else:
            self.trickle_down_max(i)

    def cngc(self, i):  # enumerate through children and grandchildren
        a = self.a
        ix = []
        for j in [i*2+1, i*2+2, i*4+3, i*4+4, i*4+5, i*4+6]:
            if j >= len(a):
                break
            ix.append((j, a[j]))
        return ix

    def trickle_down_min(self, i):  # i is on min layer
        a, f = self.a, self.key
        if i * 2 + 1 >= len(a):  # i has no children
            return
        m = min(self.cngc(i), key=lambda x: f(x[1]))[0]  # index of the smallest child or grandchild
        if a[m] < a[i]:
            a[m], a[i] = a[i], a[m]  # if m is a child of i, after the swap, min heap property at m is intact
            if m > i * 2 + 2:  # m is a grandchild of i
                j = (m - 1) // 2  # parent of m, child of i
                if a[m] > a[j]:
                    a[m], a[j] = a[j], a[m]  # after the swap, max heap property at j is intact
                self.trickle_down_min(m)

    def trickle_down_max(self, i):  # i is on max layer
        a, f = self.a, self.key
        if i * 2 + 1 >= len(a):  # i has no children
            return
        m = max(self.cngc(i), key=lambda x: f(x[1]))[0]  # index of the largest child or grandchild
        if a[m] > a[i]:
            a[m], a[i] = a[i], a[m]  # if m is a child of i, after the swap, max heap property at m is intact
            if m > i * 2 + 2:  # m is a grandchild of i
                j = (m - 1) // 2  # parent of m, child of i
                if a[m] < a[j]:
                    a[m], a[j] = a[j], a[m]  # after the swap, min heap property at j is intact
                self.trickle_down_max(m)

    def heapify(self):
        for i in rev_range(len(self.a)):
            # order is not important, as long as heap property is maintained for all layers
            self.bubble_up(i)
            self.trickle_down(i)

    def add(self, item):
        self.a.append(item)
        self.bubble_up(len(self.a) - 1)

    def peek_min(self):
        if not self.a:
            raise KeyError
        return self.a[0]

    def pop_min(self):
        a = self.a
        if not a:
            raise KeyError
        a[0], a[-1] = a[-1], a[0]
        r = a.pop()
        self.trickle_down(0)
        return r

    def peek_max(self):
        if not self.a:
            raise KeyError
        return max(self.a[:3], key=self.key)

    def pop_max(self):
        a = self.a
        if not a:
            raise KeyError
        i = argmax(a[:3], key=self.key)
        a[i], a[-1] = a[-1], a[i]
        r = a.pop()
        self.trickle_down(i)
        return r

    def verify(self):
        a, f = self.a, self.key
        n = len(a)
        for i in range(ceil((n - 1) / 2)):  # the second half of heap does not have children
            assert i * 2 + 1 < len(a)
            if self.min_layer(i):
                if any(f(a[i]) > f(x) for _, x in self.cngc(i)):
                    return False
            elif any(f(a[i]) < f(x) for _, x in self.cngc(i)):
                return False
        return True

if __name__ == '__main__':
    from math import floor
    from random import shuffle
    for size in [x for x in range(25) for _ in range(x)]:
        rnd_test = list(range(size)) * 2
        shuffle(rnd_test)
        h = MinMaxHeap(rnd_test[:size//2])
        assert h.verify()
        for x in rnd_test[size//2:]:
            h.add(x)
            assert h.verify()
        i, j = 0, size - 1
        while h:
            assert h.pop_min() == floor(i)
            assert h.verify()
            assert h.pop_max() == ceil(j)
            assert h.verify()
            i += 1 / 2
            j -= 1 / 2
