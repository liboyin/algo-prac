def gcd(x, y):
    while y > 0:
        x, y = y, x % y
    return x

def search(a, b, x, y):
    """
    Consider the infinite sequence of am + x: [a+x, 2a+x, ..., ab+x, ...], and of bn + y: [b+y, 2b+y, ..., ab+y, ...].
    Returns the minimum absolute difference between any pair of elements, i.e. min(abs((am + x) - (bn + y))).
    Observation:
        1. min(abs((am + x) - (bn + y))) = min(abs((x - y) + (am - bn))).
        2. (am - bn) is a linear combination of a and b.
        3. The set of linear combinations of a and b equals the set of multiples of gcd(a, b).
    :param a: int, positive
    :param b: int, positive
    :param x: int, non-negative
    :param y: int, non-negative
    :return: int
    """
    assert a > 0 and b > 0
    assert x >= 0 and y >= 0
    g = gcd(a, b)
    diff = abs(x - y) % g
    return min(diff, g - diff)

if __name__ == '__main__':
    assert search(a=6, b=16, x=5, y=2) == 1
