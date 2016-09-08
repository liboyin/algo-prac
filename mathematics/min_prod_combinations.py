from heapq import merge
from itertools import groupby, islice

def search(n):  # multiples of 2, 3, 5
    a = [1]
    i2 = i3 = i5 = 0
    for i in range(n - 1):
        v2, v3, v5 = 2 * a[i2], 3 * a[i3], 5 * a[i5]
        x = min(v2, v3, v5)
        a.append(x)
        if x == v2:
            i2 += 1
        if x == v3:
            i3 += 1
        if x == v5:
            i5 += 1
    return a

def search2(pf, n):  # TODO: review
    a = [1]
    merged = merge(*map(lambda p: (x * p for x in a), pf))
    unique = (x for x, _ in groupby(merged))
    list(map(a.append, islice(unique, n-1)))
    return a

if __name__ == '__main__':
    from random import sample
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    def control(pf, n):  # O(|pf| ^ n)
        s = {1}
        for _ in range(n):
            s.update({p * x for x in s for p in pf})
        return sorted(s)[:n]
    assert search(100) == search2([2, 3, 5], 100)
    assert search2([2, 7, 13, 19], 12) == [1, 2, 4, 7, 8, 13, 14, 16, 19, 26, 28, 32]
    for size in [x for x in range(5) for _ in range(x)]:
        pf = sample(primes, size)
        assert search2(pf, size * 5) == control(pf, size * 5)
