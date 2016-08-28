from math import inf

def search(xs, ys):
    """
    Returns a list of pairs (x, y), where x is in xs, y is in ys, and the list is sorted by x + y.
    Time complexity is O(mn). Space complexity is O(m).
    :param xs: list[num], sorted
    :param ys: list[num], sorted
    :return: list[tuple[num,num]]
    """
    m = len(xs)
    n = len(ys)
    r = [None] * (m * n)
    idx = [0] * m  # idx[i]: for xs[i], next possible index of match in ys
    c = 0  # next possible match is (xs[c], ys[idx[c]])
    for i in range(len(r)):
        min_val = inf
        for j in range(m):
            if idx[j] == n:
                continue
            temp = xs[j] + ys[idx[j]]
            if temp < min_val:
                min_val = temp
                r[i] = xs[j], ys[idx[j]]  # r[i] may be overwritten
                c = j
            if idx[j] == 0:
                break
        idx[c] += 1
    return r

if __name__ == '__main__':
    for k, v in {((1, 7, 11), (2, 4, 6)): [(1, 2), (1, 4), (1, 6), (7, 2), (7, 4), (7, 6), (11, 2), (11, 4), (11, 6)],
                 ((1, 1, 2), (1, 2, 3)): [(1, 1), (1, 1), (1, 2), (1, 2), (2, 1), (1, 3), (1, 3), (2, 2), (2, 3)],
                 ((1, 2), (3,)): [(1, 3), (2, 3)]}.items():
        assert search(*k) == v
