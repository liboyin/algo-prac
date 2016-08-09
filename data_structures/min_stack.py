class MinStack:  # linear extra space solution
    def __init__(self):
        self.s = []  # normal stack
        self.a = []  # auxiliary non-increasing subsequence of stack, starting from self.s[0]

    def __len__(self):
        return len(self.s)

    def __iter__(self):
        return iter(self.s)

    def __repr__(self):
        return 'stack={}, aux={}'.format(self.s, self.a)

    def push(self, item):
        self.s.append(item)
        if len(self.a) == 0 or item <= self.a[-1]:
            self.a.append(item)

    def peek_top(self):
        return self.s[-1]

    def peek_min(self):
        return self.a[-1]

    def pop(self):
        if len(self.s) == 0:
            raise IndexError
        temp = self.s.pop()
        if temp == self.a[-1]:
            self.a.pop()
        return temp

class MinStack2:  # constant extra space solution. requires numerical elements
    def __init__(self):
        self.s = []  # normal stack
        self.e = None  # min element so far

    def __len__(self):
        return len(self.s)

    def __iter__(self):  # requires linear extra space
        ms = MinStack2()
        ms.s = list(self.s)
        ms.e = self.e
        return iter([ms.pop() for _ in range(len(self.s))][::-1])

    def __repr__(self):
        return 'stack={}, min_element={}'.format(self.s, self.e)

    def push(self, item):
        if self.e is None:  # empty stack
            self.s.append(item)
            self.e = item
        elif item >= self.e:  # including when item is the second instance of the min element
            self.s.append(item)
        else:  # when finished, s[-1] < self.e
            self.s.append(item * 2 - self.e)
            self.e = item

    def peek_top(self):
        return max(self.s[-1], self.e)

    def peek_min(self):
        return self.e

    def pop(self):
        if len(self.s) == 0:
            raise IndexError
        if self.s[-1] >= self.e:  # handles multiple instances of the min element
            return self.s.pop()
        temp = self.e
        self.e = self.e * 2 - self.s[-1]
        del self.s[-1]
        if len(self.s) == 0:
            self.e = None
        return temp

if __name__ == '__main__':
    from random import randint
    for _ in range(100):
        control = []
        ms1 = MinStack()
        ms2 = MinStack2()
        rnd_test = [randint(-i-10, i+10) for i in range(100)]
        for x in rnd_test:
            control.append(x)
            ms1.push(x)
            ms2.push(x)
            assert len(control) == len(ms1) == len(ms2)
            assert control == list(iter(ms1)) == list(iter(ms2))
            assert control[-1] == ms1.peek_top() == ms2.peek_top()
            assert min(control) == ms1.peek_min() == ms2.peek_min()
        for x in rnd_test:
            assert control.pop() == ms1.pop() == ms2.pop()
            assert len(control) == len(ms1) == len(ms2)
            assert control == list(iter(ms1)) == list(iter(ms2))
            if len(control) > 0:
                assert control[-1] == ms1.peek_top() == ms2.peek_top()
                assert min(control) == ms1.peek_min() == ms2.peek_min()
