class Link:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, n):
        assert n > 0
        self.n = n
        self.d = dict()  # dict[key,Link]
        self.h = None  # Link: pointer to head of looped linked list

    def delete(self, x):  # remove x from the linked list
        if x.next is x:
            self.h = None
        else:
            x.prev.next = x.next
            x.next.prev = x.prev

    def insert(self, x):  # insert x as head of linked list
        if self.h is None:
            self.h = x.prev = x.next = x
        else:
            head, tail = self.h, self.h.prev
            tail.next = x
            x.prev = tail
            x.next = head
            head.prev = x
            self.h = x

    def move_to_head(self, x):
        if x is self.h:
            return
        if x is self.h.prev:  # same shortcut does not apply when x is h.next, as h and h.next need to be reversed
            self.h = x
        else:
            self.delete(x)
            self.insert(x)

    def get(self, key):
        x = self.d.get(key, None)
        if x is None:
            return -1
        self.move_to_head(x)
        return x.val

    def set(self, key, value):
        if self.h is None:  # initial update
            x = Link(key, value)
            self.insert(x)
            self.d[key] = x
        elif key in self.d:  # update & move to head
            x = self.d[key]
            x.val = value
            self.move_to_head(x)
        else:  # key is not in self.d
            if len(self.d) == self.n:  # LRU is full
                oldest = self.h.prev
                self.delete(oldest)
                del self.d[oldest.key]  # as self.d has a max size, dead cells will be continuously created, increasing
                # the chance of hash collisions. however, as only live entries are copied when the size of hash table
                # increases, the performance of hash table remains amortised O(1)
            new = Link(key, value)
            self.insert(new)
            self.d[key] = new
