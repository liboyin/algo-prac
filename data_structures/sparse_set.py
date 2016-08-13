import numpy as np

class SparseDict:
    """
    A restricted version of hash table, where keys are non-negative integers with a known upper bound.
    Time complexity is amortised O(1) for creation, insertion, lookup, deletion, and cleanup.
    """
    def __init__(self, upper_bound):  # universe is [0, upper_bound)
        self.sparse = np.empty(upper_bound, dtype=int)  # fixed size, randomly initialised in constant time
            # in contrast, initialisation and clean-up takes linear time for hash table due to array clean-up
        self.dense = []  # list[int,T]. the first element is a reverse pointer to sparse

    def __len__(self):
        return len(self.dense)

    def __repr__(self):
        return 'sparse = {}\ndense = {}\nn = {}'.format(self.sparse, self.dense, len(self.dense))

    def __contains__(self, key):
        return self.look_up(key) is not None

    def __getitem__(self, key):
        x = self.look_up(key)
        if x is None:
            raise KeyError
        return x[1]

    def look_up(self, key):
        assert 0 <= key < len(self.sparse)
        i = self.sparse[key]
        if 0 <= i < len(self.dense):
            x = self.dense[i]
            if x[0] == key:
                return x
        return None

    def __setitem__(self, key, val):
        if key in self:
            self.dense[self.sparse[key]] = key, val
        else:
            self.sparse[key] = len(self.dense)
            self.dense.append((key, val))

    def __delitem__(self, key):
        if key not in self:
            raise KeyError
        i = self.sparse[key]  # index of key in dense
        if i < len(self.dense) - 1:  # if the element to be deleted is not dense[-1]
            self.sparse[self.dense[-1][0]] = i  # self.dense[-1][0]: index of dense[-1] in sparse
            self.dense[i] = self.dense[-1]  # move dense[-1] to the hole
        del self.dense[-1]
        self.sparse[key] = -1  # break the pointer loop

    def __iter__(self):
        return self.keys()

    def items(self):  # order is not preserved once __delitem__ has been called
        return iter(self.dense)

    def keys(self):
        for k, v in self.items():
            yield k

    def values(self):
        for k, v in self.items():
            yield v

    def clear(self):
        self.dense = []

class SparseSet(SparseDict):
    def __init__(self, upper_bound):
        super().__init__(upper_bound)

    def add(self, *items):
        for x in items:
            self[x] = True

    def discard(self, *items):
        for x in items:
            if x in self:
                del self[x]

if __name__ == '__main__':  # TODO: random test?
    s = SparseSet(9)
    s.add(8, 6, 3, 1)
    for x in (8, 6, 3, 1):
        assert x in s
    print(s)
    s.discard(3, 6, 2)
    for x in (3, 6):
        assert x not in s
    for x in (8, 1):
        assert x in s
    print(s)
