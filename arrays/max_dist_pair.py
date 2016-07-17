from lib import rev_range, stated_map

def search(arr):
    """
    Returns the maximum j – i, s.t. arr[i] <= arr[j].
    Time complexity is O(n). Space complexity is O(n).
    :param arr: list[T], where T is comparable
    :return: int, non-negative
    """
    left_min = list(stated_map(min, arr, arr[0]))
    right_max = list(stated_map(max, reversed(arr), arr[-1]))[::-1]
    # since left_min[i] and right_max[i] are both inclusive for i, left_min[i] <= right_max[i]
    i, j = 0, 0  # two moving boundaries, where i <= j
    max_dist = 0
    while j < len(arr):
        if left_min[i] <= right_max[j]:
            max_dist = max(max_dist, j - i)
            j += 1
        else:
            i += 1  # if arr is monotonously decreasing, then i and j increase alternatively
    return max_dist

if __name__ == '__main__':
    def control(arr):
        a, n = [], len(arr)
        for i, x in enumerate(arr):
            a.append(next(j for j in rev_range(i, n) if arr[j] >= x))
        return max([x - i for i, x in enumerate(a)])
    from random import randint
    std_test = {(34, 8, 10, 3, 2, 80, 30, 33, 1): (1, 7),
                (9, 2, 3, 4, 5, 6, 7, 8, 18, 0): (0, 8),
                (1, 2, 3, 4, 5, 6): (0, 5),
                (6, 5, 4, 3, 2, 1): (0, 0)}  # arr -> i, j. multiple solutions may exist
    for k, v in std_test.items():
        assert search(k) == v[1] - v[0]
    for _ in range(1000):
        a = [randint(0, 20) for _ in range(10)]
        assert search(a) == control(a)
