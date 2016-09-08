from lib import bin_search_right, snd

def search(arr):
    """
    Given a list of tasks, represented as tuple of starting time, finishing time, and profit (non-negative). Returns
        the maximum profit achievable by choosing non-conflicting tasks.
    Solution is binary search on tasks sorted by finishing time.
    Time complexity is O(n\log n). Space complexity is O(n).
    :param arr: list[tuple[num,num,num]]. requires unique finishing time
    :return: num
    """
    if not arr:
        return 0
    a = sorted(arr, key=snd)  # sort on finishing time
    dp = [0]  # dp[i]: max profit considering a[:i]. when finished, len(dp) == n + 1
    for i, x in enumerate(a):
        start, _, val = x
        j = bin_search_right(a, start, right=i, key=snd) - 1
        # j: index (in arr) of the last task that finishes before the starting time of this one
        if j == -1:  # no task finishes before the starting time of this one
            dp.append(max(dp[-1], val))  # carry over from the previous, or start a new sequence of tasks
        else:
            dp.append(max(dp[-1], dp[j+1] + val))  # j + 1 is the index of j in dp
    return dp[-1]

if __name__ == '__main__':
    from itertools import compress, product
    from lib import fst, sliding_window
    from random import randint
    def control(arr):  # O(n 2^n)
        def step(mask):
            a = sorted(compress(arr, mask), key=fst)  # selected tasks, sorted by starting time
            if all(x[1] <= y[0] for x, y in sliding_window(a, 2)):
                return sum(x[2] for x in a)
            return 0
        return max(step(m) for m in product(*([(0, 1)] * len(arr))))
    for k, v in {((3, 10, 20), (1, 2, 50), (6, 19, 100), (10, 100, 200)): 270,
                 ((3, 10, 20), (1, 2, 50), (6, 19, 100), (2, 100, 200)): 250}.items():
        assert search(k) == v
    for size in range(15):
        a = []
        for _ in range(size):
            start = randint(0, size)
            a.append((start, randint(start+1, size*2), randint(0, size*2)))
        assert search(a) == control(a)
