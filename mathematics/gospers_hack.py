def gospers_hack(n):
    """
    HAKMEM 175, or Gosper's Hack:
    Returns the next integer with the same number of 1-bits, i.e. the next bit string permutation.
    :param n: int, positive
    :return: int, positive
    """
    assert n > 0  # negative n is not supported as Python does not have >>>
    lowest = n & -n  # lowest 1-bit of n
    left = n + lowest  # sets the last non-trailing 0-bit in n to 1, and clears its right hand side. left has no more 1-bits than n
    changed = left ^ n  # there are at least 2 1-bits in changed: the least significant bit is lowest, which changed
    # from 1 to 0; and the most significant bit changed from 0 to 1. all 1-bits between them indicate 1 -> 0 changes.
    # hence, all 1-bits in changed forms a contiguous block
    right = (changed // lowest) >> 2  # the number of 1-bits that need to be appended to the right equals the length
    # of the 1-bits block in changed minus 2 (for the head and the tail)
    return left | right  # combines left and right

if __name__ == '__main__':
    x = 5
    for _ in range(5):
        print(x, bin(x))
        x = gospers_hack(x)
