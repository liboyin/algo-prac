def is_lucky(x):
    """
    Perform the following sieve operations on the sequence of all positive integers:
    1. Remove every second integer: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, ...]
    2. Remove every third integer: [1, 3, 7, 9, 13, 15, 19, ...]
    3. Remove every fourth integer: [1, 3, 7, 13, 15, 19, ...]
    After infinitely many steps, remaining integers are lucky numbers.
    :param x: int
    :return: bool
    """
    assert x > 0
    gap = 2
    while gap <= x:
        if x % gap == 0:
            return False
        x -= x // gap  # x: number of surviving integers
        gap += 1
    return True

if __name__ == '__main__':
    lucky_nums = {1, 3, 7, 13, 19, 27, 39, 49, 63, 79, 91, 109, 133, 147, 181, 207, 223, 253, 289, 307, 349, 387, 399,
                  459, 481, 529, 567, 613, 649, 709, 763, 807, 843, 927, 949}  # up to 1000
    for x in range(1, 1000):
        if x in lucky_nums:
            assert is_lucky(x)
        else:
            assert not is_lucky(x)
