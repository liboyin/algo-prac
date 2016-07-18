def little_endian_bits(x):
    assert x >= 0
    if x == 0:
        yield False
        return
    while x > 0:
        yield bool(x & 1)
        x >>= 1

def big_endian_bits(x):
    return list(little_endian_bits(x))[::-1]

def three_divisible(bits):
    """
    Returns whether the integer represented by a bit stream is divisible by three. Endian is not important.
    Solution is FSA. The FSA contains 3 states: 0, 1, and 2, each corresponding to the remainder, divided by 3, of the
        integer represented by a partial big-endian bit stream.
    The FSA starts and terminates at state 0. Transition rules are as follows:
        s0 + 0 -> s0, s0 + 1 -> s1
        s1 + 0 -> s2, s1 + 1 -> s0
        s2 + 0 -> s2, s2 + 1 -> s1
    Since the sequence of input does not affect the final result, this algorithm accepts both big-endian and
        little-endian bit streams as input.
    This method also applies to other divisibility problems, but endian is important.
    :param bits: iterable[bool]
    :return: bool
    """
    rem = 0  # rem in {0, 1, 2}
    for x in bits:
        rem = ((rem << 1) + int(x)) % 3  # priority of left shift is lower than plus
    return rem == 0

def five_divisible(bits, LE=False):
    """
    Returns whether the integer represented by a bit stream is divisible by five.
    The solution is inspired by the trick to decide whether a base-10 number is divisible by 11:
        47278: 4 - 7 + 2 - 7 + 8 = 0. hence 47278 is a multiple of 11 (47278 = 11 * 4298)
        52214: 5 - 2 + 2 - 1 + 4 = 8. hence 52214 is not a multiple of 11 (52214 = 11 * 4746 + 8)
    This problem is equivalent to determining the 5-divisibility of a stream of base-4 numbers.
    Note that although the sequence of base-4 numbers does not affect the final result, nor does adding a 0 to the
        end of the bit stream, 2 bits in reverse order results in different base-4 numbers.
    :param bits: iterable[bool]
    :param LE: bool. True if the input bit stream is little-endian
    :return: bool
    """
    ite = iter(bits)
    rem, mul = 0, 1
    for x in ite:
        if LE:
            y = (int(next(ite, False)) << 1) + int(x)
        else:
            y = (int(x) << 1) + int(next(ite, False))
        rem = (rem + y * mul) % 5
        mul *= -1
    return rem == 0

def seven_divisible(x):
    """
    Returns whether a given integer is divisible by seven.
    Observation: (10 * a + b) % 7 == 0 <-> (20 * a + 2 * b) % 7 == 0 <-> (21 * a - a + 2 * b) % 7 == 0
                 <-> (-a + 2 * b) % 7 == 0 <-> (a - 2 * b) % 7 == 0
    :param x: int
    :return: bool
    """
    if x < 0:
        return seven_divisible(-x)
    if x == 0 or x == 7:
        return True
    if x < 10:
        return False
    div, rem = divmod(x, 10)
    return seven_divisible(div - 2 * rem)

if __name__ == '__main__':
    for x in range(10000):
        assert three_divisible(big_endian_bits(x)) == (x % 3 == 0)
        assert three_divisible(little_endian_bits(x)) == (x % 3 == 0)
        assert five_divisible(big_endian_bits(x)) == (x % 5 == 0)
        assert five_divisible(little_endian_bits(x), LE=True) == (x % 5 == 0)
        assert seven_divisible(x) == (x % 7 == 0)
