from lib import is_sorted, rev_range

def with_repeat(arr):  # output is sorted lexicographically
    assert is_sorted(arr)
    n = len(arr)
    yield arr
    while True:
        k = next((i for i in rev_range(n-1) if arr[i] < arr[i+1]), None)  # k: largest index s.t. a[k] < a[k+1]
        if k is None:  # end of lexicographical sort has been reached
            break
        l = next(i for i in rev_range(k+1, n) if arr[k] < arr[i])  # largest index l > k, s.t. a[k] < a[l]. guaranteed to exist as a[k] < a[k+1]
        arr[k], arr[l] = arr[l], arr[k]  # swap arr[k] and arr[l]
        i, j = k + 1, n - 1  # reverse arr[k+1:]
        while i < j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        yield arr

def without_repeat(arr):  # output is not sorted lexicographically
    def step(i):
        yield arr
        if i < n - 1:
            for j in range(i, n):  # anchor point
                for k in range(j+1, n):  # fixing arr[:i], swap arr[j] and arr[k]
                    arr[j], arr[k] = arr[k], arr[j]
                    yield from step(j+1)  # recursive generator
                    arr[j], arr[k] = arr[k], arr[j]
    n = len(arr)
    return step(0)

def without_repeat2(arr):  # Heap's algorithm. output is not sorted lexicographically
    def step(i):
        if i == 1:
            yield arr
        else:
            for j in range(i-1):
                yield from step(i-1)  # recursive generator
                k = j if i % 2 == 0 else 0  # if i is even, swap arr[i-1] with arr[j]; otherwise, swap with arr[0]
                arr[k], arr[i-1] = arr[i-1], arr[k]
            yield from step(i - 1)
    n = len(arr)
    if n == 0:
        return
    return step(n)  # step(i): generate permutations of arr[:i]

def without_repeat3(arr):  # Steinhaus–Johnson–Trotter algorithm. output is not sorted lexicographically
    def max_mobile_elem():  # an element is mobile iff the adjacent element on its direction is smaller
        a = [i for i in range(1, n-1) if arr[i] > arr[i+dir[i]]]
        if dir[0] == 1 and arr[0] > arr[1]:  # for arr[0], compare rightwards only. requires len(arr) > 1
            a.append(0)
        if dir[-1] == -1 and arr[-2] < arr[-1]:  # for arr[-1], compare leftwards only
            a.append(n - 1)
        return max(a, key=lambda i: arr[i], default=None)
    n = len(arr)
    if n <= 1:  # max_mobile_elem requires len(arr) > 1
        yield arr
        return
    dir = [-1] * n  # -1 for left, +1 for right. the adjacent element of arr[i] is arr[i+dir[i]]
    while True:
        yield arr
        m = max_mobile_elem()  # index of the max mobile element
        if m is None:
            break
        i = m + dir[m]  # backup m + dir[m] here since both arr and dir are to be updated
        arr[m], arr[i] = arr[i], arr[m]
        dir[m], dir[i] = dir[i], dir[m]
        m = i
        for i in range(n):  # switch direction of all elements larger than arr[m]
            if arr[i] > arr[m]:
                dir[i] *= -1

def gospers_hack(n):
    """
    HAKMEM 175, or Gosper's Hack:
    Returns the next smallest integer with the same number of 1-bits, i.e. the next bit string permutation.
    :param n: int, positive
    :return: int, positive
    """
    assert n > 0  # negative n is not supported as Python does not have >>>
    lowest = n & -n  # lowest 1-bit of n
    left = n + lowest  # sets the last non-trailing 0-bit in n to 1, and clears its right hand side. left has no more 1-bits than n
    changed = left ^ n  # there are at least 2 1-bits in changed: the least significant bit is lowest, which changed
    # from 1 to 0; and the most significant bit changed from 0 to 1. all 1-bits between them indicate 1 -> 0 changes.
    # hence, all 1-bits in changed forms a contiguous block
    right = (changed // lowest) >> 2  # the number of 1-bits that need to be appended to the right equals the length
    # of the 1-bits block in changed minus 2 (for the head and the tail)
    return left | right  # combines left and right

if __name__ == '__main__':
    # a = list('ABC')
    # for i, x in enumerate(with_repeat(a)):
    #     print(i, x)
    # a = list('ABCDE')
    # for i, x in enumerate(without_repeat3(a)):
    #     print(i, x)
    x = 5
    for _ in range(5):
        print(x, bin(x))
        x = gospers_hack(x)
