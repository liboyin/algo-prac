def next_higher(n):
    """
    HAKMEM 175, or Gosper's Hack:
    Returns the next higher integer with the same number of 1-bits, i.e. the next item in the lexicographically sorted
        bit string permutation.
    Time complexity is O(1). Space complexity is O(1).
    :param n: int, positive
    :return: int, positive
    """
    assert n > 0  # negative n is not supported as Python does not have >>>
    lowest = n & -n  # lowest 1-bit of n
    left = n + lowest  # sets the last non-trailing 0-bit in n to 1, and zeros its right hand side. after the addition,
        # there are no more 1-bits in left than in n
    changed = left ^ n  # there are at least 2 1-bits in changed: the least significant bit is lowest, which changed
        # from 1 to 0; and the most significant bit changed from 0 to 1. all 1-bits between them indicate 1 -> 0
        # changes. hence, all 1-bits in changed forms a contiguous block
    right = (changed // lowest) >> 2  # the number of 1-bits that need to be appended to the right equals the length
        # of the 1-bits block in changed minus 2 (for the head and the tail)
    return left | right  # combines left and right

def next_lower(n):
    """
    Reverse Gosper's Hack (TAOCP volume 4A 7.1.3, Q21):
    Returns the next lower integer with the same number of 1-bits, i.e. the previous item in the lexicographically
        sorted bit string permutation.
    Time complexity is O(1). Space complexity is O(1).
    :param n: int, positive
    :return: int, positive
    """
    assert n > 0  # negative n is not supported as Python does not have >>>
    inc = n + 1  # case 1: n ends with a 0-bit; case 2: n ends with a 1-bit
    right = inc ^ n  # bits that were changed during the addition. for case 1, right = 1; for case 2, right is a
        # contiguous block of 1-bits starting from 1
    left = inc & n  # 1-bits that were not changed during the addition, i.e. 1-bits on the left
    return left - (left & -left) // (right + 1)  # equivalent to left - ((left & -left) >> m), where m is the number of
        # 1-bits in right. hence, interpreting n as (1[01]*)(0+)(1*), the last 1-bit in group 1 is shifted to the least
        # significant position in group 2

if __name__ == '__main__':
    x = 7
    for _ in range(50):
        print(x, bin(x))
        x = next_higher(x)
    print('----------')
    for _ in range(50):
        print(x, bin(x))
        x = next_lower(x)
