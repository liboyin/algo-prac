from functools import reduce
from itertools import tee
from operator import xor

def repeat_two(iterable):
    """
    Given an iterable, in which all elements but one appear twice. Returns the unique element.
    Observation: x XOR x == 0. Also, since XOR is associative & commutative, order is not important.
    :param iterable: iter[int]
    :return: num
    """
    return reduce(xor, iterable, 0)

def repeat_three(iterable):  # all elements but one appear 3 times
    ones, twos = 0, 0
    for x in iterable:
        twos |= ones & x  # when x appears the first time, x is not recorded; second time, x is recorded; third time, x is recorded
        ones ^= x  # when x appears the first time, x is recorded; second time, x is cleared; third time, x is recorded
        mask = ~(ones & twos)  # zeros common 1-bits between ones and twos. only works when x appears the third time
        ones &= mask
        twos &= mask
    return ones

def two_uniques(iterable):  # all elements but two appear twice
    ite1, ite2 = tee(iterable, 2)
    acc = reduce(xor, ite1, 0)
    last = acc & -acc
    a, b = 0, 0
    for x in ite2:
        if x & last:
            a ^= x
        else:
            b ^= x
    return a, b

if __name__ == '__main__':
    from lib import unique_randints
    from random import shuffle
    for size in range(1, 100):  # number of repeating elements
        repeat = unique_randints(0, 100, size)
        unique = repeat[-1] + 1
        rep2 = repeat * 2
        rep2.append(unique)
        shuffle(rep2)
        rep3 = repeat * 3
        rep3.append(unique)
        shuffle(rep3)
        assert repeat_two(rep2) == repeat_three(rep3) == unique
        rep2.append(unique + 1)
        shuffle(rep2)
        assert set(two_uniques(rep2)) == {unique, unique + 1}
