from math import ceil, log2

def one_bits(n):
    """
    Returns the number of 1s in the binary representation of a non-negative integer.
    Brian Kernighan’s algorithm. Note that x - 1 toggles all bits starting from the last 1-bit (inclusive). This has the
        same effect as n -= n & -n, which is used in Fenwick tree.
    Time complexity is O(\log n). Space complexity is O(1).
    :param n: int, non-negative
    :return: int
    """
    assert n >= 0
    c = 0
    while n > 0:
        n &= n - 1  # zeros the last 1-bit
        c += 1
    return c

def one_bits2(n):
    assert n >= 0
    for i, x in [(1,  0b01010101010101010101010101010101),
                 (2,  0b00110011001100110011001100110011),
                 (4,  0b00001111000011110000111100001111),
                 (8,  0b00000000111111110000000011111111),
                 (16, 0b00000000000000001111111111111111)]:
        n = (n & x) + ((n >> i) & x)
    return n

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
    for n in range(1000):
        assert one_bits(n) == one_bits2(n) == bin(n)[2:].count('1')
    for i in range(1, 100):
        print(i, is_bleak(i))
