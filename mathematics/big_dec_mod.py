from functools import reduce

def mod(xs, y):
    """
    Given a big decimal number x represented as a big-endian array, calculate x % y.
    Observation: mod is distributive. Let x = 10 * x1 + x2:
    x % y = (10 * x1 + x2) % y
          = ((10 * x1) % y + x2 % y) % y
          = ((10 * (x1 % y)) % y + x2 % y) % y
          = ((10 * (x1 % y) + x2) % y) % y
          = (10 * (x1 % y) + x2) % y
    Time complexity is O(n). Space complexity is O(1).
    :param xs: list[int], non-negative
    :param y: int, positive
    :return: int, non-negative
    """
    return reduce(lambda s, x: (10 * s + x) % y, xs, 0)

def mul_mod(x, y, m):
    """
    Calculates (x * y) % m, where all three variables are in long type.
    Observation: x = x1 << 32 + x2, y = y1 << 32 + y2, where x1, x2, y1, y2 are 32-bit ints.
        This is equivalent to x = x1 * k + x2, y = y1 * k + y2, where k = 1 << 32. Then:
        x * y % m = x1 * y1 * k * k % m + x1 * y2 * k % m + x2 * y1 * k % m + x2 * y2 % m
        The multiplication of two 32-bit ints won't overflow a long type. Denote any of them by z:
        z * k % m = z * (2 ** 32) % m = ((z % m * 2) % m * 2)... for 32 times.
    Time complexity is O(1). Space complexity is O(1).
    :param x: long
    :param y: long
    :param m: long
    :return: long
    """
    def shift_n_mod(z, n):
        z %= m
        for _ in range(n):
            z = z * 2 % m
        return z
    x %= m
    y %= m
    mask = (1 << 32) - 1  # 32 1-bits
    x1 = x >> 32  # left 32 bits
    x2 = x & mask  # right 32 bits
    y1 = y >> 32
    y2 = y & mask
    a = x2 * y2 % m
    b = shift_n_mod(x1 * y2, 32)
    c = shift_n_mod(x2 * y1, 32)
    d = shift_n_mod(x1 * y1, 64)
    return (((a + b) % m + c) % m + d) % m

if __name__ == '__main__':
    from mathematics.next_greater_int import int_to_arr as to_big_endian_arr
    from random import randint
    for _ in range(1000):
        x = randint(0, 1 << 64)
        y = randint(1, 1 << 8)
        assert mod(to_big_endian_arr(x), y) == x % y
    for _ in range(1000):
        x = randint(1 << 32, 1 << 64)
        y = randint(1 << 32, 1 << 64)
        m = randint(1 << 32, 1 << 64)
        assert mul_mod(x, y, m) == x * y % m
