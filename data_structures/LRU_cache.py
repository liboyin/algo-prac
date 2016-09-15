from collections import OrderedDict

class Link:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None

class LRUCache:  # re-implementation of functools.lru_cache
    def __init__(self, n):
        assert n > 0
        self.n = n  # max size
        self.d = dict()  # dict[K,Link]: query hash table
        self.h = None  # Link: pointer to the head (most recently accessed entry) of looped linked list

    def remove_link(self, x):  # remove x from the linked list
        if x.next is x:
            self.h = None
        else:
            x.prev.next = x.next
            x.next.prev = x.prev

    def ins_to_head(self, x):  # insert x as head of linked list
        if self.h is None:
            self.h = x.prev = x.next = x
        else:
            head, tail = self.h, self.h.prev
            tail.next = x
            x.prev = tail
            x.next = head
            head.prev = x
            self.h = x

    def move_to_head(self, x):  # moves x to the head of linked list
        if x is self.h:  # x is already the head
            return
        if x is self.h.prev:  # same shortcut does not apply when x is h.next, as h and h.next need to be reversed
            self.h = x
        else:
            self.remove_link(x)
            self.ins_to_head(x)

    def __getitem__(self, key):
        """
        If (key, val) is in the LRU cache, returns val, and moves (key, val) to the head of looped linked list.
        Raises a KeyError if (key, val) is not in the LRU cache.
        Time complexity is O(1).
        :param key: K
        :return: V
        """
        x = self.d[key]
        self.move_to_head(x)
        return x.val

    def __setitem__(self, key, val):
        """
        Adds (key, val) pair to the head of the LRU cache.
        Time complexity is O(1).
        :param key: K
        :param val: V
        """
        if self.h is None:  # initial update
            new = Link(key, val)
            self.ins_to_head(new)
            self.d[key] = new
        elif key in self.d:  # update & move to head
            x = self.d[key]
            x.val = val
            self.move_to_head(x)
        else:  # key is not in self.d
            if len(self.d) == self.n:  # LRU is full
                oldest = self.h.prev
                self.remove_link(oldest)
                del self.d[oldest.key]  # as self.d has a max size, dead cells will be continuously created, increasing
                # the chance of hash collisions. however, as only live entries are copied when the size of hash table
                # increases, the performance of hash table remains amortised O(1)
            new = Link(key, val)
            self.ins_to_head(new)
            self.d[key] = new

class LRU_Cache2:
    def __init__(self, n):
        self.d = OrderedDict()  # OrderedDict is implemented as unordered dict + linked list
        self.n = n

    def __getitem__(self, key):
        v = self.d.pop(key)
        self.d[key] = v
        return v

    def __setitem__(self, key, val):
        if key in self.d:
            self.d.pop(key)
        else:
            if self.n > 0:
                self.n -= 1
            else:
                self.d.popitem(last=False)
        self.d[key] = val
