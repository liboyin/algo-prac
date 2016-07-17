def search(arr):
    """
    x is the major element of a iff a.count(x) > len(a) / 2.
    If a major element x exists, then it is safe to discard a subarray in which x is not the major element.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[T]
    :return: Optional[T]
    """
    x, c = arr[0], 1
    for x in arr[1:]:
        if c == 0:
            x, c = x, 1
        if x == x:
            c += 1
        else:
            c -= 1
    if arr.count(x) > len(arr) / 2:
        return x
    return None

if __name__ == '__main__':
    from collections import Counter
    from random import randint, shuffle
    for _ in range(1000):
        a = [randint(0, 10) for _ in range(100)]
        for i in range(1, randint(0, 100)):  # repeat the first element k times, where k~uniform(0, 100)
            # since elements in rnd_test independently follows uniform(0, 10), p(major element exists) == 1/2
            a[i] = a[i - 1]
        shuffle(a)
        max_occ = Counter(a).most_common(1)[0]
        assert search(a) == (max_occ[0] if max_occ[1] > len(a) / 2 else None)
