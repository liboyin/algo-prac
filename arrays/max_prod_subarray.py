def search(arr):
    min_prod, max_prod = 1, 1
    global_max = 1
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
            min_prod, max_prod = 1, 1  # hard reset
        global_max = max(global_max, max_prod)
    if global_max > 1:
        return global_max
    return max(arr)

if __name__ == '__main__':
    from functools import reduce
    from operator import mul
    from random import randint
    def control(arr):
        n = len(arr)
        m = arr[0]
        for i in range(n):
            for j in range(i, n):
                m = max(m, reduce(mul, arr[i: j+1], 1))
        return m
    std_test = {(6, -3, -10, 0, 2): (0, 2, 180),
                (-1, -3, -10, 0, 60): (4, 4, 60),
                (-2, -3, 0, -2, -40): (3, 4, 80),
                (1, -2, -3, 0, 7, -8, -2): (4, 6, 112)}
    for k, v in std_test.items():
        assert search(k) == v[2]
    for _ in range(100):
        a = [randint(-10, 10) for _ in range(100)]
        assert search(a) == control(a)
