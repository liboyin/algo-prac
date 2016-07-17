from itertools import chain
from math import inf
from random import randint

class Infinity:
    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

class Node:
    def __init__(self, key, val, parent=None, pseudo_root=None, priority=None):
        self.key = key
        self.val = val
        self.left = None  # left.key < right.key. duplication is not allowed
        self.right = None
        self.parent = parent
        self.pseudo_root = pseudo_root
        self.priority = randint(0, 7919) if priority is None else priority  # max-heap on priority

    def __iter__(self):
        assert self is not self.pseudo_root
        left_iter = () if self.left is None else iter(self.left)  # (): tuple of length 0
        right_iter = () if self.right is None else iter(self.right)
        return chain(left_iter, ((self.key, self.val),), right_iter)  # (x,): tuple of length 1

    def __repr__(self):
        assert self is not self.pseudo_root
        left_repr = 'None' if self.left is None else repr(self.left)
        right_repr = 'None' if self.right is None else repr(self.right)
        return '({}, {}:{}, {}, {})'.format(left_repr, self.key, self.val, self.priority, right_repr)

    def rotate_left(self):  # (left, self, (rl, right, rr)) -> ((left, self, rl), right, rr)
        assert self is not self.pseudo_root
        assert self.right is not None
        temp = self.right
        self.right = temp.left
        if self.right is not None:
            self.right.parent = self
        if self is self.parent.left:
            self.parent.left = temp
        else:
            self.parent.right = temp
        temp.parent = self.parent
        self.parent = temp
        temp.left = self

    def rotate_right(self):  # ((ll, left, lr), self, right) -> (ll, left, (lr, self, right))
        assert self is not self.pseudo_root
        assert self.left is not None
        temp = self.left
        self.left = temp.right
        if self.left is not None:
            self.left.parent = self
        if self is self.parent.left:
            self.parent.left = temp
        else:
            self.parent.right = temp
        temp.parent = self.parent
        self.parent = temp
        temp.right = self

    def insert_left(self, key, val):
        # self is pseudo_root if the Treap is currently empty
        self.left = Node(key, val, self, self.pseudo_root)
        self.left.bubble_up()

    def insert_right(self, key, val):
        assert self is not self.pseudo_root
        self.right = Node(key, val, self, self.pseudo_root)
        self.right.bubble_up()

    def bubble_up(self):
        assert self is not self.pseudo_root
        if self.priority > self.parent.priority:
            if self is self.parent.left:
                self.parent.rotate_right()
            else:
                self.parent.rotate_left()
            self.bubble_up()

    def delete(self):
        assert self is not self.pseudo_root
        self.trickle_down()  # not the same as normal BST
        if self is self.parent.left:
            self.parent.left = None
        else:
            self.parent.right = None

    def trickle_down(self):
        assert self is not self.pseudo_root
        if self.left is None and self.right is None:
            return
        left_priority = -1 if self.left is None else self.left.priority  # requires priority to be >= 0
        right_priority = -1 if self.right is None else self.right.priority
        if left_priority < right_priority:
            self.rotate_left()
        else:
            self.rotate_right()
        self.trickle_down()

    def verify(self):
        assert self is not self.pseudo_root
        if self.left is None or (self.priority >= self.left.priority and self.left.verify()):
            if self.right is None or (self.priority >= self.right.priority and self.right.verify()):
                return True if (self.left is None or self.right is None) else self.left.key < self.right.key
        return False

class Treap:
    def __init__(self):
        self.pseudo_root = Node(key=Infinity(), val=None, priority=inf)
        # all key comparisons must have node key or parent key on the left hand side
        self.pseudo_root.pseudo_root = self.pseudo_root
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.size == 0:
            return iter(())  # empty iterator is not equivalent to StopIteration
        return iter(self.pseudo_root.left)

    def __repr__(self):
        if self.size == 0:
            return '()'
        return repr(self.pseudo_root.left)

    def look_up(self, key):
        x = self.pseudo_root
        while x is not None:
            if x.key > key:
                x = x.left
            elif x.key < key:
                x = x.right
            else:
                return x
        return None

    def __contains__(self, key):
        return self.look_up(key) is not None

    def __getitem__(self, key):
        x = self.look_up(key)
        if x is None:
            raise KeyError
        return x.val

    def __setitem__(self, key, val):
        x = self.pseudo_root
        while True:
            if x.key > key:
                if x.left is None:
                    x.insert_left(key, val)
                    self.size += 1
                    break
                x = x.left
            elif x.key < key:
                if x.right is None:
                    x.insert_right(key, val)
                    self.size += 1
                    break
                x = x.right
            else:
                x.val = val

    def __delitem__(self, key):
        x = self.look_up(key)
        if x is None:
            raise KeyError
        x.delete()
        self.size -= 1

    def get_min(self, pop=False):
        if self.size == 0:
            raise KeyError
        x = self.pseudo_root.left
        while x.left is not None:
            x = x.left
        k, v = x.key, x.val
        if pop:
            x.delete()
            self.size -= 1
        return k, v

    def get_max(self, pop=False):
        if self.size == 0:
            raise KeyError
        x = self.pseudo_root.left
        while x.right is not None:
            x = x.right
        k, v = x.key, x.val
        if pop:
            x.delete()
            self.size -= 1
        return k, v

    def verify(self):
        if self.size == 0:
            return True
        return self.pseudo_root.left.verify()

if __name__ == '__main__':
    from random import shuffle
    tp = Treap()
    control = set()
    arr = list(range(250)) * 4
    shuffle(arr)
    for x in arr:
        if x in control:
            assert x in tp
            assert tp[x] == x + 42
            del tp[x]
            assert x not in tp
            control.remove(x)
        else:
            assert x not in tp
            tp[x] = x + 42
            assert x in tp
            control.add(x)
        assert len(tp) == len(control)
        assert tp.verify()
        assert set(x[0] for x in tp) == control
        if len(tp) > 0:
            assert tp.get_min()[0] == min(control)
            assert tp.get_max()[0] == max(control)
    assert len(tp) == 0
