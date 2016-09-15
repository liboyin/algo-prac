from lib import yield_while

class Link:
    def __init__(self, key, right=None):
        self.key = key
        self.right = right

class LinkedList:
    def __init__(self, seq):
        ite = iter(seq)
        x = next(ite, None)
        assert x is not None
        self.head = last = Link(x)
        for x in ite:
            new = Link(x)
            last.right = new
            last = new

    def reverse(self):
        h, r = self.head, None  # h, r: tail and head of the reversed sublist
        while h:
            h.right, r, h = r, h, h.right
        self.head = r

    def __iter__(self):
        for y in yield_while(self.head, bool, lambda x: x.right):
            # since __bool__ is not defined in Link, bool(link) is always True unless link is None
            yield y.key

def remove_duplicates(head):  # in-place, O(n^2) time
    left = head
    while left is not None:
        probe = left  # inspect probe.right
        while probe is not None:
            if probe.right is not None and probe.right.key == left.key:
                probe.right = probe.right.right
            else:  # if probe.right is removed, then do not move forward. consider [0, -6, 7, 4, 5, -6, -6]
                probe = probe.right
        left = left.right

if __name__ == '__main__':
    from lib import iter_equals
    from random import randint
    def control(arr):
        appeared = set()
        for x in arr:
            if x not in appeared:
                yield x
            appeared.add(x)
    for size in [x for x in range(50) for _ in range(x)]:
        a = [randint(-size, size) for _ in range(size)]
        ll = LinkedList(reversed(a))
        ll.reverse()
        assert iter_equals(ll, a)
        remove_duplicates(ll.head)
        assert iter_equals(ll, control(a))
