from lib import stated_map

def search(arr):
    """
    Returns the maximum j – i, where arr[i] <= arr[j].
    Time complexity is O(n). Space complexity is O(n).
    :param arr: list[T], where T is comparable
    :return: int, non-negative
    """
    assert len(arr) > 0
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
    from lib import rev_range
    from random import randint
    def control(arr):  # O(n^2)
        a, n = [], len(arr)
        for i, x in enumerate(arr):
            a.append(next(j for j in rev_range(i, n) if arr[j] >= x))
        return max(x - i for i, x in enumerate(a))
    for k, v in {(34, 8, 10, 3, 2, 80, 30, 33, 1): (1, 7),  # arr -> i, j. multiple solutions may exist
                (9, 2, 3, 4, 5, 6, 7, 8, 18, 0): (0, 8),
                (1, 2, 3, 4, 5, 6): (0, 5),
                (6, 5, 4, 3, 2, 1): (0, 0)}.items():
        assert search(k) == v[1] - v[0]
    for size in range(1, 100):
        a = [randint(0, size) for _ in range(size)]
        assert search(a) == control(a)
