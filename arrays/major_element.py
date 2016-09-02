def search(arr):
    """
    x is the major element of a iff a.count(x) > len(a) / 2.
    Observation: If a major element x exists, then it is safe to discard a subarray in which x is not the major element.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[T], where T is comparable
    :return: Optional[T]
    """
    e, c = None, 0
    for x in arr:
        if c == 0:
            e = x
        c += 1 if e == x else -1
    return e if arr.count(e) > len(arr) / 2 else None

def search_3(arr):  # TODO: random test?
    """
    Find all elements that appear more than n / 3 times.
    Observation: There are at most two such major elements.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[T], where T is comparable
    :return: tuple[*T]
    """
    e1 = e2 = None
    c1 = c2 = 0
    for x in arr:
        if c1 == 0 and x != e2:
            e1 = x
        elif c2 == 0 and x != e1:
            e2 = x
        if x == e1:
            c1 += 1
        elif x == e2:
            c2 += 1
        else:
            c1 -= 1
            c2 -= 1
    n = len(arr)
    return (x for x in (e1, e2) if x is not None and arr.count(x) > n / 3)

if __name__ == '__main__':
    from collections import Counter
    from random import randint, shuffle
    for _ in range(1000):
        a = [randint(0, 10) for _ in range(100)]
        for i in range(1, randint(0, 100)):  # repeat the first element k times, where k~uniform(0, 100)
            # since elements in rnd_test independently follows uniform(0, 10), p(major element exists) == 1/2
            a[i] = a[i-1]
        shuffle(a)
        head = Counter(a).most_common(2)[0]
        assert search(a) == (head[0] if head[1] > len(a) / 2 else None)
