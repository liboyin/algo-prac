import heapq
from lib import is_sorted

def search(xs, ys):
    """
    Given two sorted arrays, generates (x, y) pairs s.t. x is in xs, y is in ys, and x * y are in increasing order.
    Time complexity is O(mn\log (mn)). Space complexity is O(mn).
    Note that any solution that allows duplication has a time complexity no lower than O(mn).
    :param xs: list[num], sorted
    :param ys: list[num], sorted
    :return: generator[tuple[num,num]]
    """
    assert is_sorted(xs) and is_sorted(ys)
    m, n = len(xs), len(ys)
    if m * n == 0:
        return
    h = [(xs[0] + ys[0], 0, 0)]
    v = {(0, 0)}  # visited indices
    while True:
        if len(h) == 0:
            break
        _, i, j = heapq.heappop(h)
        yield xs[i], ys[j]
        if i < m - 1 and (i+1, j) not in v:
            heapq.heappush(h, (xs[i+1] + ys[j], i + 1, j))
            v.add((i+1, j))
        if j < n - 1 and (i, j+1) not in v:
            heapq.heappush(h, (xs[i] + ys[j+1], i, j + 1))
            v.add((i, j+1))

if __name__ == '__main__':
    from itertools import zip_longest
    for k, v in {((1,7,11), (2,4,6)):
                 ((1,2),(1,4),(1,6),(7,2),(7,4),(11,2),(7,6),(11,4),(11,6)),
                 ((1,1,2), (1,2,3)):
                 ((1,1),(1,1),(1,2),(2,1),(1,2),(2,2),(1,3),(1,3),(2,3)),
                 ((1,2), (3,)): ((1,3),(2,3))}.items():
        for x, y in zip_longest(search(*k), v):
            assert sum(x) == sum(y)
