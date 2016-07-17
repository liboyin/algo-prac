from math import ceil, log2

def one_bits(x):
    """
    Returns the number of 1s in the binary representation of a non-negative integer.
    Brian Kernighan’s algorithm. Note that x - 1 toggles all bits starting from the last 1-bit (inclusive). This has the
        same effect as n -= n & -n, which is used in Fenwick tree.
    Time complexity is O(\log n). Space complexity is O(1).
    :param x: int, non-negative
    :return: int
    """
    assert x >= 0
    c = 0
    while x > 0:
        x &= x - 1  # zeros the last 1-bit
        c += 1
    return c

def is_bleak(x):
    """
    A positive integer x is bleak if there does not exist y <= n, s.t. x == y + one_bits(y)
    :param x: int, positive
    :return: bool
    """
    assert x > 0
    for y in range(x - ceil(log2(x)), x):  # the greatest # of 1-bits in any y <= x is ceil(log_2(x))
        if y + one_bits(y) == x:
            return False
    return True

if __name__ == '__main__':
    for i in range(1, 100):
        print(i, is_bleak(i))
