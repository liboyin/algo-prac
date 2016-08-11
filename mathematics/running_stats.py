import heapq

class RunningMedian:
    def __init__(self):
        self.left = []  # list[T], where T is comparable. max heap of elements smaller than or equal to mid
        # self.left is implemented as a min heap of negative elements since heapq only supports min heap
        self.right = []  # list[T]. min heap of elements larger than or equal to mid
        self.mid = None

    def __len__(self):
        if self.mid is None:
            return 0
        return len(self.left) + len(self.right) + 1

    def push_left(self, item):
        heapq.heappush(self.left, -item)

    def pop_left(self):
        return -heapq.heappop(self.left)

    def push_right(self, item):
        heapq.heappush(self.right, item)

    def pop_right(self):
        return heapq.heappop(self.right)

    def accept(self, item):
        """
        Returns the left median of the input sequence so far. Denote the input sequence by seq, let n = len(seq):
        If n is odd, returns sorted(seq)[n//2]; otherwise, returns sorted(seq)[n/2-1].
        Note that left median only requires T to be comparable, whereas true median requires divisibility by 2.
        Over n calls, time complexity is O(n\log n), space complexity is O(n).
        :param item: T, comparable
        :return: T
        """
        if self.mid is None:  # n == 0
            self.mid = item
            return item
        if len(self.left) == 0:
            if len(self.right) == 0:  # n == 1
                self.push_right(max(self.mid, item))
                self.mid = min(self.mid, item)
            else:  # n == 2
                xs = sorted([self.mid, self.right[0], item])
                self.push_left(xs[0])
                self.mid, self.right[0] = xs[1:]
            return self.mid
        # at this stage, 0 < len(self.left) <= len(self.right). equality holds iff n is odd
        left_max, right_min = -self.left[0], self.right[0]
        if len(self.left) < len(self.right):  # n is even
            if item <= self.mid:
                self.push_left(item)
            elif self.mid < item <= right_min:
                self.push_left(self.mid)
                self.mid = item
            else:  # right_min < item
                self.push_right(item)
                self.push_left(self.mid)
                self.mid = self.pop_right()
        else:  # len(self.left) == len(self.right). n is even
            if item < left_max:
                self.push_left(item)
                self.push_right(self.mid)
                self.mid = self.pop_left()
            elif left_max <= item < self.mid:
                self.push_right(self.mid)
                self.mid = item
            else:  # self.mid <= item
                self.push_right(item)
        return self.mid

class RunningAverage:
    def __init__(self):
        self.mean = 0
        self.n = 0

    def __len__(self):
        return self.n

    def accept(self, item):
        n = self.n  # shorthand
        self.mean = self.mean / (n+1) * n + item / (n+1)  # may be less precise
        self.n += 1
        return self.mean

if __name__ == '__main__':
    from random import shuffle
    for size in [x for x in range(50) for _ in range(x)]:
        rnd_test = list(range(size)) * 2
        shuffle(rnd_test)
        rm = RunningMedian()
        ra = RunningAverage()
        for i in range(len(rnd_test)):
            assert rm.accept(rnd_test[i]) == sorted(rnd_test[:i+1])[i//2]
            assert abs(ra.accept(rnd_test[i]) - sum(rnd_test[:i+1])/(i+1)) < 0.00001
