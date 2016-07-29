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

if __name__ == '__main__':
    from random import randint
    for _ in range(10000):
        bound = 1 << 64
        x = randint(0, bound)
        y = randint(0, bound)
        assert x + y == add(x, y)
        assert x * y == mul(x, y)
