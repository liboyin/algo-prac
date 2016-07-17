from lib import bin_search_left
from operator import itemgetter as get_item

def search(arr):
    """
    Given a list of tasks, represented as tuple of starting time, finishing time, and value.
    Selects tasks maximising total value, s.t. finishing time of task i is no later than the starting time of task i+1.
    Solution is binary search on tasks sorted by finishing time.
    Time complexity is O(n\log n). Space complexity is O(n\log n).
    :param arr: list[tuple[num,num,num]]
    :return: num
    """
    n = len(arr)
    if n == 0:
        return 0
    arr = sorted(arr, key=get_item(1))
    dp = [0] * n  # dp[i]: max weight executing task i, having considered arr[:i]
    dp[0] = arr[0][2]
    for i, x in enumerate(arr[1:], start=1):
        start, _, val = x
        prev = bin_search_left(arr, start, right=i, key=get_item(1))
        # prev: index (in arr) of the last task that has finished before the starting time of this one
        if prev == 0:  # no task finishes before the starting time of this one
            dp[i] = val
        else:
            dp[i] = dp[prev-1] + val  # bin_search returns the insertion point, hence prev - 1
    return max(dp)

if __name__ == '__main__':
    assert search([(3, 10, 20), (1, 2, 50), (6, 19, 100), (10, 100, 200)]) == 270
    assert search([(3, 10, 20), (1, 2, 50), (6, 19, 100), (2, 100, 200)]) == 250
