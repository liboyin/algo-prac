from math import inf

def add(x, y):
    """
    Adds two non-negative integers using only bitwise operators.
    Negative numbers are not supported due to Python's autocast. Consider -1 + 1 in 2-compliment form.
    Equivalent recursive version: add(x, y) = x if y == 0 else add(x ^ y, (x & y) << 1)
    Time complexity is O(n). Space complexity is O(1).
    :param x: int, non-negative
    :param y: int, non-negative
    :return: int
    """
    assert x >= 0 and y >= 0
    while y != 0:
        x, y = x ^ y, (x & y) << 1
    return x

def mul(x, y):
    """
    Multiplies two non-negative integers using only bitwise operators.
    Time complexity is O(n^2). Space complexity is O(1).
    :param x: int, non-negative
    :param y: int, non-negative
    :return: int
    """
    assert x >= 0 and y >= 0
    r = 0
    while y > 0:
        if y & 1:
            r = add(r, x)
        x <<= 1
        y >>= 1
    return r

def int_div(x, y):
    """
    Divides two integers using bitwise operators and arithmetic minus.
    Note that Python integer division is floored when the result is negative. e.g. 8 / -7 = -2.
    Time complexity is O(\log n). Space complexity is O(1).
    :param x: int
    :param y: int
    :return: int
    """
    if x == 0:
        return -1 if y == 0 else 0  # 0 / 0 = -1; 0 / x = 0
    if y == 0:
        return inf if x > 0 else -inf  # x / 0 = \inf
    if x < 0:
        return int_div(-x, -y) if y < 0 else -int_div(-x, y) - 1  # -x / -y = x / y; -x / y = -(x / y)
    if y < 0:
        return -int_div(x, -y) - 1  # x / -y = -(x / y)
    if x < y:
        return 0
    if x == y:
        return 1
    if y == 1:
        return x
    # reverse bit multiplication
    assert x > y > 0
    i, y1 = 0, y
    while y1 <= x:
        i += 1
        y1 <<= 1
    r = 0
    while y1 >= y:
        if x >= y1:
            x -= y1
            r |= 1 << i
        i -= 1
        y1 >>= 1
    return r

if __name__ == '__main__':
    from random import choice, randint
    for _ in range(10000):
        bound = 1 << 64
        x = randint(0, bound)
        y = randint(0, bound)
        assert x + y == add(x, y)
        assert x * y == mul(x, y)
        x *= choice((-1, 1))
        y *= choice((-1, 1))
        assert x // y == int_div(x, y), (x, y, x // y, int_div(x, y))
