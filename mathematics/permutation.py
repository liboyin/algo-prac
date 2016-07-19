from lib import is_sorted, rev_range

def with_repeat(arr):  # output is sorted lexicographically
    assert is_sorted(arr)
    n = len(arr)
    yield arr
    while True:
        k = next((i for i in rev_range(n-1) if arr[i] < arr[i+1]), None)  # k: largest index s.t. a[k] < a[k+1]
        if k is None:  # arr is reversely sorted
            return
        l = next(i for i in rev_range(k+1, n) if arr[k] < arr[i])
        # largest index l > k, s.t. a[k] < a[l]. guaranteed to exist as a[k] < a[k+1]
        arr[k], arr[l] = arr[l], arr[k]  # swap arr[k] and arr[l]
        i, j = k + 1, n - 1  # reverse arr[k+1:]
        while i < j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        yield arr

def without_repeat(arr):  # output is not sorted
    def step(i):
        yield arr
        if i >= n - 1:  # handles n == 0
            return
        for j in range(i, n):
            for k in range(j+1, n):  # fixing arr[:i], swap every possible pairs
                arr[j], arr[k] = arr[k], arr[j]
                yield from step(j+1)  # recursive call, in which arr[:j+1] is fixed
                arr[j], arr[k] = arr[k], arr[j]
    n = len(arr)
    yield from step(0)

def without_repeat2(arr):  # Heap's algorithm. output is not sorted
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

def without_repeat3(arr):  # Steinhaus–Johnson–Trotter algorithm. output is not sorted
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
            return
        i = m + dir[m]  # backup m + dir[m] here since both arr and dir are to be updated
        arr[m], arr[i] = arr[i], arr[m]
        dir[m], dir[i] = dir[i], dir[m]
        m = i
        for i in range(n):  # switch direction of all elements larger than arr[m]
            if arr[i] > arr[m]:
                dir[i] *= -1

if __name__ == '__main__':
    a = list('ABCDE')
    for i, x in enumerate(with_repeat(a)):
        print(i, x)
    a = list('ABCDE')
    for i, x in enumerate(without_repeat3(a)):
        print(i, x)
