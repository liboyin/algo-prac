def search(xs, ys):
    """
    Given two arrays of positive integers, find the number of (x, y) pairs, s.t. x ^ y > y ^ x.
    Observation: For all (x, y), xy > 1. Hence, x ^ y > y ^ x <-> x ^ (1/x) > y ^ (1/y).
    Time complexity is O(m\log m + n\log n) from sorting. Space complexity is O(m+n).
    :param xs: list[int], positive
    :param ys: list[int], positive
    :return: int
    """
    assert all(x >= 1 for x in xs)
    assert all(y >= 1 for y in ys)
    xs = sorted(x ** (1/x) for x in xs)
    ys = sorted(y ** (1/y) for y in ys)
    n = len(ys)
    i, c = 0, 0  # i: cursor on ys; c: counter
    for x in xs:
        while i < n and x > ys[i]:
            i += 1
        c += i
    return c

if __name__ == '__main__':
    assert search([2, 1, 6], [1, 5]) == 3
