import heapq
from lib import filter3, is_sorted, safe_query
from math import inf

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
        Note that left median only requires T to be comparable, whereas true median requires division.
        Time complexity is O(\log n), space complexity is O(n).
        :param item: T
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
        self.mean = self.mean / (n+1) * n + item / (n+1)
        self.n += 1
        return self.mean

def median_of_two_sorted(xs, ys):
    """
    Returns the true median of the merge of two sorted arrays. Let arr = sorted(xs + ys), n = len(arr):
    If n is odd, returns arr[n//2]; otherwise, returns (arr[n/2-1] + arr[n/2]) / 2.
    Time complexity is O(\log n).
    :param xs: list[num]. sorted
    :param ys: list[num]. sorted
    :return: num
    """
    assert is_sorted(xs) and is_sorted(ys)
    n = len(xs) + len(ys)
    assert n > 0
    right_median = kth_of_two_sorted(xs, ys, n // 2 + 1)  # k starts from 1
    if n % 2 == 1:
        return right_median
    left_median = kth_of_two_sorted(xs, ys, n // 2)
    return (left_median + right_median) / 2

def kth_of_two_sorted(xs, ys, k):  # expected O(n) time
    assert is_sorted(xs) and is_sorted(ys)
    assert 0 < k <= len(xs) + len(ys)
    if len(xs) == 0:
        return ys[k - 1]
    if len(ys) == 0:
        return xs[k - 1]
    if k == 1:
        return min(xs[0], ys[0])
    h = k // 2
    if safe_query(xs, h-1, inf) < safe_query(ys, h-1, inf):
        return kth_of_two_sorted(xs[h:], ys, k - h)  # recursive call
    return kth_of_two_sorted(xs, ys[h:], k - h)  # recursive call

def kth(arr, k):  # expected O(n) time, worst case O(n^2) time
    assert 0 < k <= len(arr)  # k is cardinal
    lt, eq, gt = filter3(arr[len(arr)//2], arr)
    if k <= len(lt):
        return kth(lt, k)  # recursive call
    elif k > len(lt) + len(eq):
        return kth(gt, k - len(lt) - len(eq))  # recursive call
    else:  # 0 < k - len(lt) <= len(eq)
        return eq[k - 1 - len(lt)]  # order is stable

if __name__ == '__main__':
    from random import randint, shuffle
    # test RunningMedian and RunningAverage
    for _ in range(100):
        rnd_test = list(range(100)) * 2
        shuffle(rnd_test)
        rm = RunningMedian()
        ra = RunningAverage()
        for i in range(len(rnd_test)):
            assert rm.accept(rnd_test[i]) == sorted(rnd_test[:i+1])[i//2]
            assert abs(ra.accept(rnd_test[i]) - sum(rnd_test[:i+1])/(i+1)) < 0.00001
    # test median_of_two_sorted and kth_of_two_sorted
    for size in range(100):
        left = sorted(randint(-size, size) for _ in range(size))
        right = sorted(randint(-size, size) for _ in range(size+1))
        merge = sorted(left + right)
        for i, x in enumerate(merge):
            assert kth_of_two_sorted(left, right, i + 1) == x
        if len(merge) % 2 == 0:
            assert median_of_two_sorted(left, right) == (merge[len(merge) / 2 - 1] + merge[len(merge) / 2]) / 2
        else:
            assert median_of_two_sorted(left, right) == merge[len(merge) // 2]
    # test kth
    for _ in range(100):
        rnd_test = [randint(-100, 100) for _ in range(100)]
        for i, x in enumerate(sorted(rnd_test)):
            assert kth(rnd_test, i + 1) == x
