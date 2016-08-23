from lib import rev_range

def insert(arr, start, finish):
    """
    Given a non-overlapping sequence of intervals, denoted as (start, finish) pairs, and sorted by start time,
        inserts a new interval.
    Observation: since intervals are non-overlapping, end times are sorted too.
    Time complexity is O(n). Space complexity is O(n).
    :param arr: list[tuple[num, num]], sorted
    :param start: num, non-negative
    :param finish: num, positive. start < finish
    :return: list[tuple[num, num]]
    """
    n = len(arr)
    left = next((i for i in range(n) if arr[i][1] >= start), None)  # last interval that finishes no earlier than the
        # start of the new interval. all intervals in arr[:left] finish before the start of the new interval
    if left is None:  # all intervals have finished when the new interval starts
        return arr + [(start, finish)]
    new_start = min(arr[left][0], start)  # arr[left] is either fully or partially contained in the new interval
    right = next((i for i in rev_range(n) if arr[i][0] <= finish), None)  # first interval that starts no later than
        # the finish of the new interval. all intervals in arr[right+1:] start after the finish of the new interval
    if right is None:  # no interval has started when the new interval ends
        return [(start, finish)] + arr
    new_end = max(arr[right][1], finish)
    return list(arr[:left]) + [(new_start, new_end)] + list(arr[right+1:])

def insert2(arr, start, finish):
    r = []
    new = start, finish
    for x in arr:
        if x[1] < new[0]:
            r.append(x)
        elif new[1] < x[0]:
            r.append(new)
            new = x
        else:
            assert x[1] >= new[0] or new[1] <= x[0]
            new = min(x[0], new[0]), max(x[1], new[1])
    r.append(new)
    return r

if __name__ == '__main__':
    from lib import randints
    for k, v in {(((1, 3), (6, 9)), 2, 5): [(1, 5), (6, 9)],
                 (((1, 2), (3, 5), (6, 7), (8, 10), (12, 16)), 4, 9): [(1, 2), (3, 10), (12, 16)]}.items():
        assert insert(*k) == insert2(*k) == v
    for size in [x for x in range(50) for _ in range(x)]:
        ite = iter(randints(0, size * 10, size * 2))
        a = list(zip(ite, ite))  # [1, 2, 3, 4, 5, 6] -> [(1, 2), (3, 4), (5, 6)]
        start, finish = sorted(randints(0, size * 10, 2))
        assert insert(a, start, finish) == insert2(a, start, finish)
