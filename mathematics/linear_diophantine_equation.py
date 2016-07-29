def ext_euclid(a, b):
    """
    Returns gcd(a, b) as a linear combination of a and b. Such a decomposition is unique.
    :param a: int, positive
    :param b: int, positive
    :return: tuple[int,int,int]. a * x + b * y == q == gcd(a, b)
    """
    if b == 0:
        return 1, 0, a
    div, rem = divmod(a, b)
    x, y, q = ext_euclid(b, rem)
    x, y = y, (x - div * y)
    return x, y, q

def ext_euclid2(a, b):
    print('a={}, b={}'.format(a, b))
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        div, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - div * x1
        y0, y1 = y1, y0 - div * y1
    return x0, y0, a

def linear_diophantine_equation(a, b, c):  # TODO: not tested
    """
    Finds integer x & y, s.t. a * x + b * y == c. Returns (None, None) if solution does not exist.
    Observation: Solution to a linear diophantine equation exists iff gcd(a, b) divides c.
    :param a: int
    :param b: int
    :param c: int
    :return: tuple[int,int] or tuple[None,None]
    """
    x, y, q = ext_euclid(a, b)
    if c % q == 0:
        k = c / q
        return x * k, y * k
    return None, None

if __name__ == '__main__':
    from mathematics.min_diff_of_multiples import gcd
    from random import randint
    std_test = {(35, 15): (1, -2, 5),
                (240, 46): (-9, 47, 2),
                (30, 47): (11, -7, 1)}  # this is a good example to try the algorithm by hand
    for k, v in std_test.items():
        assert ext_euclid2(*k) == v
    for _ in range(1000):
        a, b = randint(1, 1 << 31), randint(1, 1 << 31)
        x, y, q = ext_euclid2(a, b)
        assert x * a + y * b == q == gcd(a, b)
