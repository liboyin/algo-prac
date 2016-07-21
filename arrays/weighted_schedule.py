from lib import bin_search_right, safe_query
from operator import itemgetter as get_item

def search(arr):
    """
    Given a list of tasks, represented as tuple of starting time, finishing time, and value.
    Selects tasks maximising total value, s.t. finishing time of task i is no later than the starting time of task i+1.
    Solution is binary search on tasks sorted by finishing time.
    Time complexity is O(n\log n). Space complexity is O(n).
    :param arr: list[tuple[num,num,num]]
    :return: num
    """
    n = len(arr)
    if n == 0:
        return 0
    a = sorted(arr, key=get_item(1))  # sort on finishing time
    dp = [0] * n  # dp[i]: max profit executing task i, having considered a[:i]
    dp[0] = a[0][2]
    for i, x in enumerate(a[1:], start=1):
        start, _, val = x
        prev = bin_search_right(a, start, right=i, key=get_item(1))
        # prev: index (in arr) of the last task that has finished before the starting time of this one
        dp[i] = safe_query(dp, prev-1, 0) + val  # if prev == 0, no task finishes before the starting time of this one
    return max(dp)

if __name__ == '__main__':  # TODO: random test?
    assert search([(3, 10, 20), (1, 2, 50), (6, 19, 100), (10, 100, 200)]) == 270
    assert search([(3, 10, 20), (1, 2, 50), (6, 19, 100), (2, 100, 200)]) == 250
