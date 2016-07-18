from functools import reduce
from lib import filter_index, identity
from math import ceil, sqrt
from operator import mul

def eratosthenes(n):
    """
    Sieve of Eratosthenes. Finds all primes within [1, n].
    Time complexity is O(n\log\log n). Space complexity is O(n).
    :param n: int, positive
    :return: generator[int]
    """
    assert n > 0
    a = [True] * (n + 1)  # it is further possible to remove all even numbers
    a[0] = a[1] = False  # by definition
    for i in range(2, ceil(sqrt(n)) + 1):  # sqrt(n) leads to \log\log time complexity
        if a[i]:  # if a[i] is a known non-prime, then its multiples have been labeled non-prime already
            for j in range(2, n // i + 1):
                a[i * j] = False
    return filter_index(identity, a)

def legendre(p, n):
    """
    Legendre's formula. Given prime p and integer n >= p, returns the greatest x, s.t. p ^ x divides n!.
    Observation: In [1, n], n // p integers divide p, n // p^2 integers divide p^2, ...
    This algorithm does not work if p is not a prime, as p * f divides p for all factors f of p.
    Time complexity is O(n/p). Space complexity is O(n).
    Side note: This is the solution to question "how many tailing 0s there are in 100 factorial?".
    :param p: int, p >= 2
    :param n: int, positive
    :return: int
    """
    assert p >= 2 and n > 0
    x, p1 = 0, p
    while p1 <= n:
        x += n // p1
        p1 *= p
    return x

def search(n):
    """
    Returns number of factors of n!, including 1 and n! itself.
    Observation: The set of primal factors of n! equals the set of primes in [2, n]. For each primal factor, denoted
        by p, let x be the maximum integer, s.t. p ^ x divides n!. Then p may appear in any factor of n! in the form
        of p ^ i, where i in [0, x].
    :param n: int, positive
    :return: int
    """
    assert n > 0
    return reduce(mul, [legendre(p, n) + 1 for p in eratosthenes(n)], 1)

if __name__ == '__main__':
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
    assert list(eratosthenes(271)) == primes
    std_test = {(3, 7): 2, (3, 10): 4, (2, 16): 15, (7, 16): 2}
    for k, v in std_test.items():
        assert legendre(*k) == v
    std_test = {3: 4, 4: 8, 16: 5376}
    for k, v in std_test.items():
        assert search(k) == v
