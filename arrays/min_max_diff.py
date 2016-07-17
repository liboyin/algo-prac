from itertools import product

def search(arr, k):
    """
    Given an array of numbers, and a positive number k. For each element in arr, either increase its value by k, or
    decrease its value by k. Choose directions of update, s.t. the maximum difference between any two elements in the
    resulting array is minimised. Time complexity is O(n).
    :param arr: list[num]
    :param k: num
    :return: num
    """
    n = len(arr)
    assert n >= 0
    if n <= 1:
        return 0
    if k == 0:
        return max(arr) - min(arr)
    if k < 0:
        return search(arr, -k)
    a = [x - k for x in sorted(arr)]
    a_min, a_max = a[0], a[-1]
    min_diff = a_max - a_min
    for i in range(n):
        a[i] += k * 2
        if a_min == a[i] - k * 2:  # a[i] was the minimum
            a_min = a[0] if i == n - 1 else min(a[0], a[i+1])  # rolling min
        a_max = max(a_max, a[i])
        min_diff = min(min_diff, a_max - a_min)
    return min_diff

if __name__ == '__main__':
    def control(arr, k):
        def bf_all():
            for ds in product(*([(-k, k)] * n)):
                yield [arr[i] + ds[i] for i in range(n)]
        n = len(arr)
        r = min(bf_all(), key=lambda x: max(x) - min(x))
        return max(r) - min(r)
    from random import randint
    std_test = {((1, 5, 15, 10), 3): ((4, 8, 12, 7), 8),
                ((4, 6), 10): ((14, 16), 2),
                ((6, 10), 3): ((9, 7), 2),
                ((1, 10, 14, 14, 15), 6): ((7, 4, 8, 8, 9), 5),
                ((1, 2, 3), 2): ((3, 4, 5), 2),
                ((3, 4, 5, 6, 7, 8), 4): ((7, 8, 9, 10, 11, 12), 5),
                ((1, 5, 6, 7, 8, 9, 10), 6): ((7, -1, 0, 1, 2, 3, 4), 8),
                ((4, 6), 100): ((104, 106), 2)}  # (arr_in, k) -> (arr_out, diff)
    for k, v in std_test.items():
        assert search(*k) == v[1]
    for _ in range(100):
        a = [randint(0, 20) for _ in range(10)]
        k = randint(1, 30)
        assert search(a, k) == control(a, k)
