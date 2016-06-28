from lib import bin_search_left, yield_while
from lib import kth_of_iter as last
from math import inf, isfinite
from operator import itemgetter as get_item
from random import random

class BaseLinkedList:
    class Node:
        def __init__(self, key):
            self.key = key
            self.next = None

    def __init__(self):
        self.head = self.tail = None

    def __iter__(self):
        return yield_while(self.head.next, lambda x: x is not self.tail, lambda x: x.next)

class LinkedList(BaseLinkedList):
    class Node(BaseLinkedList.Node):
        def __init__(self, key, val):
            super().__init__(key)
            self.val = val

    def __init__(self, iterable):
        super().__init__()
        self.head = LinkedList.Node(-inf, None)
        self.tail = LinkedList.Node(inf, None)
        last = self.head
        for k, v in iterable:
            assert isfinite(k)
            last.next = LinkedList.Node(k, v)
            last = last.next
        last.next = self.tail

    def get_item(self, key, left=None, right=None):
        if right is None:
            if left is not None:
                return key, left.val
            left, right = self.head, self.tail
        last_lt = last(yield_while(left, lambda x: x.key < key, lambda x: x.next))
        if last_lt.next.key == key:
            return key, last_lt.next.val
        return None

class SampledLinkedList(BaseLinkedList):
    class Node(BaseLinkedList.Node):
        def __init__(self, key, base):
            super().__init__(key)
            self.base = base

    def __init__(self, base, p):
        super().__init__()
        self.base = base
        self.head = SampledLinkedList.Node(-inf, base.head)
        self.tail = SampledLinkedList.Node(inf, base.tail)
        last = self.head
        for x in base:
            if random() <= p:
                last.next = SampledLinkedList.Node(x.key, x)
                last = last.next
        last.next = self.tail

    def get_item(self, key, left=None, right=None):
        if right is None:
            if left is not None:
                return self.base.get_item(key, left.base)
            left, right = self.head, self.tail
        last_lt = last(yield_while(left, lambda x: x.key < key, lambda x: x.next))
        if last_lt.next.key == key:
            return self.base.get_item(key, last_lt.next.base)
        return self.base.get_item(key, last_lt.base, last_lt.next.base)

class SkipList:
    def __init__(self, arr, p=0.5):  # arr is sorted
        self.size = len(arr)
        x = LinkedList(arr)
        self.base = x
        self.top = x
        while x.head.next is not x.tail and x.head.next.next is not x.tail:  # size >= 2
            self.top = x
            x = SampledLinkedList(x, p)

    def __len__(self):
        return self.size

    def __iter__(self):
        for x in self.items():
            yield x[0]

    def items(self):
        x = self.base.head.next
        while x is not self.base.tail:
            yield x.key, x.val
            x = x.next

    def __contains__(self, key):
        return self.top.get_item(key) is not None

    def __getitem__(self, key):
        x = self.top.get_item(key)
        if x is None:
            raise KeyError
        return x[1]

class SkipArray:
    def __init__(self, arr, p=0.5):
        self.a = [list(enumerate(arr))]
        while True:
            sub = [(i, x[1]) for i, x in enumerate(self.a[-1]) if random() <= p]  # (i, x), where i is the index of x in the previous layer
            if len(sub) == 0:
                break
            if len(sub) < len(self.a[-1]):
                self.a.append(sub)

    def __iter__(self):
        return iter(self.a[0])

    def __len__(self):
        return len(self.a[0])

    def __repr__(self):
        return '\n'.join(str(x) for x in self.a)

    def index(self, item):  # expected O(\log n) time, compared to worst case O(\log n) of normal binary search
        # imaging a binary-indexed tree. searching on each layer is actually constant time; and the # of layers is logarithmic
        layer = len(self.a) - 1
        left, right = 0, len(self.a[layer])  # range of search. left is inclusive, right is exclusive
        while True:
            assert left < right
            if layer == -1:  # search failed
                return None
            al = self.a[layer]
            i = bin_search_left(al, item, left, right, key=get_item(1))
            if i < len(al) and al[i][1] == item:
                while layer > 0:
                    i = self.a[layer][i][0]  # index in the lower layer
                    layer -= 1
                return i
            else:
                layer -= 1
                if i == 0:  # for all x in al, x[1] > item
                    left, right = 0, al[0][0] + 1  # relax range to avoid left == right. otherwise right = al[0][0]
                elif i == len(al):  # for all x in al, x[1] < item
                    left, right = al[-1][0], len(self.a[layer])  # relax range. otherwise left = al[-1][0] + 1
                else:  # for all x in al[:i], x[1] < item; for all x in al[i:], x[1] > item
                    left, right = al[i-1][0], al[i][0]  # relax range. otherwise left = al[i-1][0] + 1


if __name__ == '__main__':
    from random import randint
    for _ in range(1000):
        a = sorted({randint(0, 1000) for _ in range(100)})  # no duplication. sorted returns a list
        sa = SkipArray(a)
        sl = SkipList(list(zip(a, range(len(a)))))
        for i, x in enumerate(a):
            assert x in sl
            assert i == sa.index(x) == sl[x]
