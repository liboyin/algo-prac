from lib import is_sorted, rev_range

def search(arr, gap):
    """
    For arr[i], the last element before gap is the rightmost arr[j], s.t. arr[j] + gap < arr[i].
    Returns an array of index of last element for each arr[i]. Not exist is represented by None, e.g. for arr[0].
    Time complexity is O(n). Space complexity is O(n).
    :param arr: list[num], sorted
    :param gap: num, non-negative
    :return: list[Optional[int]]
    """
    assert gap >= 0
    assert is_sorted(arr)
    n = len(arr)
    lbg = [None] * n
    if n <= 1:  # requires len(arr) >= 2
        return lbg
    i, j = n-1, n-1  # arr[i+1:] is scanned, lbg[j+1:] is filled
    while i > 0:
        while i > 0 and arr[i] + gap >= arr[j]:  # slide i leftwards
            i -= 1
        while i <= j and arr[i] + gap < arr[j]:  # slide j leftwards
            lbg[j] = i
            j -= 1
    return lbg

if __name__ == '__main__':
    std_test = {((), 1): [],
                ((2,), 1): [None],
                ((1, 2), 0): [None, 0],
                ((2, 5, 5, 9), 2): [None, 0, 0, 2]}
    for k, v in std_test.items():
        assert search(*k) == v
    from random import randint
    for size in [x for x in range(50) for _ in range(x)]:
        a = sorted(randint(-size, size) for _ in range(size))
        g = randint(0, size)
        assert search(a, g) == [next((j for j in rev_range(i) if a[j] + g < a[i]), None) for i in range(size)]
