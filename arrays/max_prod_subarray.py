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
    min_prod = max_prod = global_max = 1
    for x in arr:
        assert min_prod <= 1 and max_prod >= 1
        if x > 0:
            min_prod = min(1, min_prod * x)  # if falls in [1, inf), then reset
            max_prod = max(1, max_prod * x)  # if falls in (0, 1), then reset. not possible to fall in (-inf, 0]
        elif x < 0:
            temp = min_prod
            min_prod = max_prod * x  # not possible to fall in [1, inf)
            max_prod = max(1, temp * x)  # if falls in (-inf, 1], then reset
        else:
            min_prod = max_prod = 1  # hard reset
        global_max = max(global_max, max_prod)
    if global_max > 1:
        return global_max
    return max(arr)  # consider [0.1, -0.2, 0.3]

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
    for k, v in {(6, -3, -10, 0, 2): (0, 2, 180),
                (-1, -3, -10, 0, 60): (4, 4, 60),
                (-2, -3, 0, -2, -40): (3, 4, 80),
                (1, -2, -3, 0, 7, -8, -2): (4, 6, 112)}.items():
        assert search(k) == v[2]
    for _ in range(100):
        a = [randint(-10, 10) for _ in range(100)]
        assert search(a) == control(a)
