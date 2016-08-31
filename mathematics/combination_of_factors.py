from functools import lru_cache
from math import sqrt

def factorise(n):
    """
    Factorises a positive integer to primal factors. e.g. f(12) = [2, 2, 3]; f(13) = [13]
    Time complexity is O(sqrt(n)). Space complexity is O(sqrt(n)).
    :param n: int, positive
    :return: list[int], sorted
    """
    assert n > 0
    r = []
    i = 2
    while i <= n:
        if n % i == 0:
            r.append(i)
            n //= i
        else:
            i += 1
    return r

@lru_cache()
def search(n):  # TODO: time complexity with caching???
    """
    Finds all non-trivial (not including 1 or self) factorisations of an integer.
    :param n: int, positive
    :return: list[tuple[*int]]
    """
    r = []
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            m = n // i
            for xs in search(m):
                if xs[0] >= i:  # factors are in ascending order
                    r.append((i,) + xs)
            r.append((i, m))
    return r

if __name__ == '__main__':
    from functools import reduce
    from operator import mul
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271}
    for n in range(4, 271):
        if n in primes:
            continue
        fs_arr = search(n)
        fs_set = set(fs_arr)
        assert len(fs_arr) == len(fs_set)
        assert tuple(factorise(n)) in fs_set
        for xs in fs_arr:
            assert reduce(mul, xs, 1) == n
