import heapq
import sys

eps = sys.float_info.epsilon

class RunningMedian:
    def __init__(self):
        self.left = []  # max-heap of elements less than or equal to the median
        self.right = []  # min-heap of elements greater than or equal to the median

    def __len__(self):
        return len(self.left) + len(self.right) + 1

    def push_left(self, item):
        heapq.heappush(self.left, -item)

    def peek_left(self):
        return -self.left[0]

    def pop_left(self):
        return -heapq.heappop(self.left)

    def push_right(self, item):
        heapq.heappush(self.right, item)

    def peek_right(self):
        return self.right[0]

    def pop_right(self):
        return heapq.heappop(self.right)

    def accept(self, num):
        """
        Returns the true median of the input sequence so far. Denote the sorted input sequence by seq, let n = len(seq):
            If n is odd, returns seq[n//2]; otherwise, returns (seq[n//2-1] + seq[n//2]) / 2.
        Over n calls, time complexity is O(n\log n), space complexity is O(n).
        :param item: num
        :return: num
        """
        if len(self.left) == 0:
            self.push_left(num)
        elif len(self.left) == len(self.right):
            if num <= self.peek_right():
                self.push_left(num)
            else:
                self.push_left(self.pop_right())
                self.push_right(num)
        else:
            assert len(self.left) == len(self.right) + 1
            if num <= self.peek_left():
                self.push_right(self.pop_left())
                self.push_left(num)
            else:
                self.push_right(num)
        if len(self.left) == len(self.right):
            return (self.peek_left() + self.peek_right()) / 2
        return self.peek_left()

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
        for i in range(size * 2):
            mean = rm.accept(rnd_test[i])
            partial = sorted(rnd_test[:i+1])
            if len(partial) & 1:
                assert mean == partial[i//2]
            else:
                assert abs(mean - (partial[i//2] + partial[i//2+1]) / 2) < eps
            assert abs(ra.accept(rnd_test[i]) - sum(partial)/(i+1)) < 0.0000001  # seems to be less precise than eps
