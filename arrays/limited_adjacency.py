def search(arr):
    """
    Minimise sum, without skipping two contiguous elements.
    Time complexity is O(n). Space complexity is O(1).
    Similar logic applies to min/max sum with no adjacent selections/skips.
    :param arr: list[num]
    :return: num
    """
    if len(arr) <= 1:
        return 0
    exc, inc = 0, arr[0]  # minimum sum, excluding/including the previous element
    for x in arr[1:]:
        exc, inc = inc, min(exc, inc) + x
    return min(exc, inc)  # since only min and add are used, this algorithm also works with negative arr

def search2(arr, k):
    """
    Given k workers and a list of tasks, each taking time arr[i]. Each worker can only take continuous tasks.
    Returns the minimum total time to finish all tasks. Time complexity is O(n\log sum(arr)).
    :param arr: list[num]
    :param k: int, positive
    :return: num
    """
    def is_possible(t):  # returns whether the tasks be finished in time t
        i, remain = 0, total
        for _ in range(k):
            j = 0  # sum task for current worker
            while i < len(arr) and j + arr[i] <= t:
                j += arr[i]
                i += 1
            remain -= j
            if remain <= 0:
                return True
        return False
    assert k > 0
    total = sum(arr)
    low, high = 0, total
    while low <= high:
        mid = (low + high) // 2
        if is_possible(mid):
            high = mid - 1
        else:
            low = mid + 1
    return low

if __name__ == '__main__':
    for k, v in {(10, 5, 7, 10): 12,
                 (10,): 0,
                 (10, 30): 10,
                 (10, 5, 2, 4, 8, 6, 7, 10): 22,
                 (1, 2, 3, 4, 5, 6): 9}.items():
        assert search(k) == v
    for k, v in {((4, 5, 10), 2): 10,
                 ((10, 7, 8, 12, 6, 8), 4): 15}.items():
        assert search2(*k) == v
