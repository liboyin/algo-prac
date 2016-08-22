from random import choice

class RndMultiSet:
    def __init__(self):
        self.d = dict()  # sparse array
        self.a = []  # dense array

    def __len__(self):
        return len(self.a)

    def __repr__(self):
        return 'sparse = {}\ndense = {}'.format(self.d, self.a)

    def __contains__(self, x):
        return x in self.d

    def add(self, x):
        a, d = self.a, self.d
        n = len(a)
        if x in d:
            d[x].add(n)
        else:
            d[x] = {n}
        a.append(x)

    def remove(self, x):
        a, d = self.a, self.d
        n = len(a)
        s = d[x]  # raises KeyError if x is not in self.d
        if n - 1 in s:
            s.remove(n - 1)
        else:
            i = next(iter(s))  # remove x from an arbitrary location in self.a
            s.remove(i)
            last_i = n - 1
            last_x = a[-1]
            a[i] = last_x
            d[last_x].remove(last_i)
            d[last_x].add(i)
        del a[-1]
        if len(s) == 0:  # hence, x in self == x in self.d
            del d[x]

    def random(self):
        """
        Returns a random element in the multiset. The probability of element x being selected is proportional to the
            total number of x in the multiset. e.g. Given {2, 3, 3, 5}, p(2) = p(5) = 1/4; p(3) = 1/2.
        Raises IndexError if multiset is empty.
        :return: T
        """
        return choice(self.a)
