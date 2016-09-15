def search(arr):
    """
    Finds the product of the maximum product subarray.
    Observation: The identity element of addition is 0. In Kadane's algorithm, if a partial sum is below 0, reset to 0.
        For multiplication, the identity element is 1. Assuming non-negative elements, a similar logic can be applied:
        reset to 1 if the partial product is below 1. Here, two partial products are maintained, one for [1, inf), the
        other for (-inf, 1].
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[num]
    :return: num
    """
    assert len(arr) > 0
    min_prod = max_prod = gmax = arr[0]
    for x in arr[1:]:
        min_prod, max_prod = min(x, min_prod * x, max_prod * x), max(x, min_prod * x, max_prod * x)
        gmax = max(gmax, max_prod)
    return gmax

if __name__ == '__main__':
    from functools import reduce
    from operator import mul
    from random import randint
    def control(arr):
        n = len(arr)
        m = arr[0]
        for i in range(n):
            for j in range(i, n):
                m = max(m, reduce(mul, arr[i:j+1], 1))
        return m
    for k, v in {(-1, -1): (0, 1, 1),
                 (0.1, -0.2, 0.3): (2, 2, 0.3),
                 (6, -3, -10, 0, 2): (0, 2, 180),
                 (-1, -3, -10, 0, 60): (4, 4, 60),
                 (-2, -3, 0, -2, -40): (3, 4, 80),
                 (1, -2, -3, 0, 7, -8, -2): (4, 6, 112)}.items():
        assert search(k) == v[2]
    for size in [x for x in range(50) for _ in range(x)]:
        a = [randint(-size, size) for _ in range(size)]
        assert search(a) == control(a)
