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

if __name__ == '__main__':
    from mathematics.next_greater_int import int_to_arr  # big-endian
    from random import randint
    for _ in range(10000):
        x = randint(0, 1 << 64)
        y = randint(1, 1 << 8)
        assert mod(int_to_arr(x), y) == x % y
