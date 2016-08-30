def next_greater(arr):
    s = [0]  # list[int]. maintains as a stack the indices of a non-increasing subsequence of arr
    r = [None] * len(arr)  # list[int]. r[i]: smallest j s.t. a[j] > a[i], or None if such j does not exist
    for i, x in enumerate(arr[1:], start=1):
        while len(s) > 0 and x > arr[s[-1]]:  # for all indices y in stack s.t. arr[y] < x
            r[s.pop()] = i
        s.append(i)
    return r  # returns indices

def prev_greater(arr):
    n = len(arr)
    r = next_greater(arr[::-1])
    r.reverse()
    for i, x in enumerate(r):
        if x is not None:
            r[i] = n - 1 - x
    return r

if __name__ == '__main__':
    def control_next(arr):
        n = len(arr)
        r = [None] * n
        for i in range(n):
            for j in range(i+1, n):
                if arr[j] > arr[i]:
                    r[i] = j
                    break
        return r
    def control_prev(arr):
        n = len(arr)
        r = [None] * n
        for i in range(n):
            for j in rev_range(i):
                if arr[j] > arr[i]:
                    r[i] = j
                    break
        return r
    from lib import rev_range
    from random import shuffle
    for size in [x for x in range(50) for _ in range(x)]:
        a = list(range(size)) * 2
        shuffle(a)
        assert next_greater(a) == control_next(a)
        assert prev_greater(a) == control_prev(a)
